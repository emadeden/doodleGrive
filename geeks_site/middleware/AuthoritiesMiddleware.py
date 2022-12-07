import re

from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.deprecation import MiddlewareMixin
from accounts.models import G
from myApp.models import File


FILE_GROUP_MEMBERSHIP_REQUIRED_URLS = []
if hasattr(settings, 'FILE_GROUP_MEMBERSHIP_REQUIRED_URLS'):
    FILE_GROUP_MEMBERSHIP_REQUIRED_URLS += [re.compile(url) for url in settings.FILE_GROUP_MEMBERSHIP_REQUIRED_URLS]
    
GROUP_OWNER_REQUIRED_URLS = []
if hasattr(settings, 'GROUP_OWNER_REQUIRED_URLS'):
    GROUP_OWNER_REQUIRED_URLS += [re.compile(url) for url in settings.GROUP_OWNER_REQUIRED_URLS]
    
FILE_OWNER_REQUIRED_URLS = []
if hasattr(settings, 'FILE_OWNER_REQUIRED_URLS'):
    FILE_OWNER_REQUIRED_URLS += [re.compile(url) for url in settings.FILE_OWNER_REQUIRED_URLS]
    
GROUP_GROUP_MEMBERSHIP_REQUIRED_URLS = []
if hasattr(settings, 'GROUP_GROUP_MEMBERSHIP_REQUIRED_URLS'):
    GROUP_GROUP_MEMBERSHIP_REQUIRED_URLS += [re.compile(url) for url in settings.GROUP_GROUP_MEMBERSHIP_REQUIRED_URLS]

class checkAuthorization(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        path = request.path_info.lstrip('/')
        # get id "url parameter"
        id = view_kwargs.get('id', None)
        if id is not None:
            # file group-membership privileges reuired
            if any(m.match(path) for m in FILE_GROUP_MEMBERSHIP_REQUIRED_URLS):
                try:
                    file = get_object_or_404(File, id = id)
                    if len(list(set( file.groups.all()) & set(request.user.g_set.all()) )) == 0:
                        return JsonResponse({"status":"unauthorized"}, status = 401)
                except Exception as e:
                    return JsonResponse({"status":"Internal Server Error", "message":str(e)}, status = 500)
            # group group-membership privileges required
            elif any(m.match(path) for m in GROUP_GROUP_MEMBERSHIP_REQUIRED_URLS):
                try:
                    group = get_object_or_404(G, id = id)
                    # check if user in the group
                    group_members = group.users.all()
                    if request.user not in group_members:
                        print(group_members)
                        return JsonResponse({"status":"unauthorized"}, status = 401)
                except Exception as e:
                    return JsonResponse({"status":"Internal Server Error", "message":str(e)}, status = 500)
            # group ownership privileges reuired
            elif any(m.match(path) for m in GROUP_OWNER_REQUIRED_URLS):
                try:
                    group = G.objects.all().get(id = id )
                    # if the user is not the owner of the group return 401
                    if group.owner != request.user:
                        return JsonResponse({"status":"unauthorized"}, status = 401)
                except Exception as e:
                    return JsonResponse({"status":"Internal Server Error", "message":str(e)}, status = 500)
            # file owner privileges required
            elif any(m.match(path) for m in FILE_OWNER_REQUIRED_URLS):
                try:
                    file = get_object_or_404(File, id = id)
                    if file.owner != request.user:
                        return JsonResponse({"status":"unauthorized"}, status = 401)
                except Exception as e:
                    return JsonResponse({"status":"Internal Server Error", "message":str(e)}, status = 500)