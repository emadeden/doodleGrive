import re

from django.conf import settings
from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin


AUTHENTICATION_REQUIRED_URLS = []
if hasattr(settings, 'AUTHENTICATION_REQUIRED_URLS'):
    AUTHENTICATION_REQUIRED_URLS += [re.compile(url) for url in settings.AUTHENTICATION_REQUIRED_URLS]


class LoginRequiredMiddleware(MiddlewareMixin):
    def process_request(self, request):
        assert hasattr(request, 'user'), "The Login Required Middleware"
        if not request.user.is_authenticated:
            path = request.path_info.lstrip('/')
            if any(m.match(path) for m in AUTHENTICATION_REQUIRED_URLS):
                redirect_to_login = settings.LOGIN_URL
                return HttpResponseRedirect(redirect_to_login)
