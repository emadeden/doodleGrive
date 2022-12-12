from django.shortcuts import render ,get_object_or_404  , redirect
from django.http import HttpResponse , HttpResponseRedirect 
from django.contrib.auth.models import User
from django.conf import settings
from django.http import JsonResponse

from .forms import *
from .models import * 
from itertools import chain
from django.db import transaction
import json
# Create your views here.
import os 
import datetime
from django.db.models import Q

SITE_ROOT = os.path.dirname(os.path.realpath(__file__)) + '/..'
LOG_LEVEL = settings.LOG_LEVEL

def index(request):
    return render(request , 'index.html')

def contact(request):
    return render(request, 'contact.html')

def showMyFiles(request):
    user = request.user 
    files = File.objects.all().filter(owner = user )
    return render (request , 'home.html' , {'files':files})

def log(log_record ,log_file, level):
    if LOG_LEVEL >= level:
        with open(SITE_ROOT+'/media/logs/' + log_file) as json_file:
            data = json.load(json_file)
            data.append(log_record)
            j = json.dumps(data)
            json_file.close()
        f = open(SITE_ROOT+'/media/' + log_file, 'w')
        f.write(j)
        f.close()
        

def upload(request):
    user = request.user
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                with transaction.atomic():
                    obj = form.save(commit=False)
                    obj.owner = user
                    obj.name = str(form['name'].value())
                    obj.name = obj.name.replace(" ", "_")
                    file = request.FILES['file']
                    data = file.read()
                    obj.content = data
                    try:
                        obj.save()
                    except:
                        return HttpResponse("Error while Createing ")
                    g = G.objects.filter(id__in  = request.POST.getlist('groups'))
                    #print(request.POST.getlist('groups'))
                    for group in g :
                        group_members = group.users.all()
                        if user in group_members:
                            obj.groups.add(group)
                        else:
                            1/0
                    #record action
                    log_record = {'user': user.username  , 'method' : 'upload' , 'file_name' : obj.name , 'time_stamp': str(datetime.datetime.now())}
                    log(log_record, 'files-log.json', 1)
                    return HttpResponseRedirect("/")
            except Exception as e:
                return JsonResponse({"status":"Internal Server Error"},status = 500)
        else:
            groups = user.g_set.all()
            return render(request, 'uploadFile.html' , {'form': form , 'user': user, 'groups': groups})
    else:
        form = FileForm()
        groups = user.g_set.all()
        return render(request, 'uploadFile.html' , {'form': form , 'user': user, 'groups': groups})

# def update(request , id):
#     context ={}
#     obj = get_object_or_404(File, id = id)
#     form = FileForm(request.POST or None, instance = obj)
#     if form.is_valid():
#         form.save()
#         #log action
#         log_record = {'user': request.user.username  , 'method' : 'update' , 'file_name' : obj.name , 'time_stamp': str(datetime.datetime.now())}
#         log(log_record, 'files-log.json', 1)
#         return HttpResponseRedirect("/")
#     context["form"] = form
#     return render(request, "upload.html", context)

def update(request , id):
    context ={}
    user = request.user 
    obj = get_object_or_404(File, id = id)
    form = UpdateFileForm(request.POST or None, instance = obj)
    if form.is_valid():
        try:
            with transaction.atomic():
                g = G.objects.filter(id__in  = request.POST.getlist('groups'))
                #print(request.POST.getlist('groups'))
                for group in g :
                    group_members = group.users.all()
                    if user in group_members:
                        obj.groups.add(group)
                    else:
                        1/0
                form.save()
                #log action
                log_record = {'user': request.user.username  , 'method' : 'update' , 'file_name' : obj.name , 'time_stamp': str(datetime.datetime.now())}
                log(log_record, 'files-log.json', 1)
                return HttpResponseRedirect("/"+ str(id) + "/getFileDetail")
        except Exception as e:
                return JsonResponse({"status":"Internal Server Error"},status = 500)
            
    form.fields['groups'].queryset  = G.objects.all().filter(users__id__exact = user.pk )
    context["form"] = form
    return render(request, "upload.html", context)

def delete(request , id ):
    obj = get_object_or_404(File, id = id)
    os.remove((SITE_ROOT+'/media/'+ 'documents/' +str(obj.owner) + "/" +str(obj.name) ))
    obj.delete()
    #log action
    log_record = {'user': request.user.username  , 'method' : 'delete' , 'file_name' : obj.name , 'time_stamp': str(datetime.datetime.now())}
    log(log_record, 'files-log.json', 1)
    return JsonResponse({"status":"success","message":"file deleted successfully!"})

# def getFileDetail(request, id ):
#     user = request.user
#     obj = get_object_or_404(File, id = id)
#     groups = obj.groups.all()
#     userGroups = user.g_set.all()
#     level = 0 
#     for group in groups:
#         if userGroups.filter(id = group.id ).exists(): #l.g_set.all().filter(id = f.id).exists()
#             level = 1
#             break
#     #log action
#     log_record = {'user': request.user.username  , 'method' : 'getFileDetails' , 'file_name' : obj.name , 'time_stamp': str(datetime.datetime.now())}
#     log(log_record, 'files-log.json', 4)
#     return render(request , 'getFileDetail.html' , {'file': obj , 'user':user  , 'level':level})

def getFileDetail(request, id ):
    user = request.user
    obj = get_object_or_404(File, id = id)
    groups = obj.groups.all()
    userGroups = user.g_set.all()
    level = 0 
    for group in groups:
        if userGroups.filter(id = group.id ).exists(): #l.g_set.all().filter(id = f.id).exists()
            level = 1 
            break
    #log action
    log_record = {'user': request.user.username  , 'method' : 'getFileDetails' , 'file_name' : obj.name , 'time_stamp': str(datetime.datetime.now())}
    log(log_record, 'files-log.json', 4)
    return render(request , 'getFileDetail.html' , {'file': obj , 'user':user  , 'level':level})
    
def getGroupDetail(request, id ):
    obj = get_object_or_404(G, id = id)
    users = obj.users.all()
    files = obj.file_set.all()
    #log action
    log_record = {'user': request.user.username  , 'method' : 'getGroupDetails' , 'group_name' : obj.name , 'time_stamp': str(datetime.datetime.now())}
    log(log_record, 'groups-log.json', 4)
    return render(request , 'getGroupDetail.html' , {'group': obj , 'users':users  , 'files': files  })

# def home(request):
#     if 'file_name' in request.GET and request.GET['file_name']:
#         Files = File.objects.all().filter(name__icontains = request.GET['file_name'])
#     else:
#         Files = []
#         user = request.user
#         for file in File.objects.all():
#             if len(list(set( file.groups.all()) & set(user.g_set.all()) )) >=1:
#                 Files.append(file)
#         #allFile = File.objects.all()
#     return render(request , 'home.html' , {'files' : Files})

def home(request):
    # user authenticated
    if request.user.is_authenticated:
        user = request.user
        if 'file_name' in request.GET and request.GET['file_name']:
            allFile = File.objects.all().filter(groups__in = user.g_set.all()).distinct().filter(name__icontains = request.GET['file_name'])
        else:
           allFile = File.objects.all().filter(groups__in = user.g_set.all()).distinct()
    
    # user not authenticated
    else:
        publicGroup = G.objects.get(id = 29)
        allFile = publicGroup.file_set.all()

    return render(request , 'home.html' , {'files' : allFile})
    
def displayContent(request  , id ):
    context ={}
    obj = get_object_or_404(File, id = id)
    f= open(SITE_ROOT+'/media/'+ 'documents/' +str(obj.owner) + "/" +str(obj.name) , 'r')
    context['content'] = f.read()
    #log action
    log_record = {'user': request.user.username  , 'method' : 'displayContents' , 'file_name' : obj.name , 'time_stamp': str(datetime.datetime.now())}
    log(log_record, 'files-log.json', 4)
    return render(request , 'displayContent.html' , context)

def editContent(request , id ):
    user = request.user 
    context ={}
    obj = get_object_or_404(File, id = id)
    if obj.block is None:
        obj.block = user 
        obj.save()
    
    elif obj.block != user :
        #return HttpResponse('You Cant Edit Because the file is bocked by '+ str(obj.block))
        return JsonResponse({"status":"fail","message":"file blocked"},403)
    form = editForm(request.POST or None, instance = obj)
    if form.is_valid():
        file = SITE_ROOT+"/media/" + str(obj.file) 
        f= open(file, "w")
        f.writelines(form['content'].value())
        form.save()
        obj.block = None
        #obj.name = form['name']
        obj.save()
        #log action
        log_record = {'user': request.user.username  , 'method' : 'editContent' , 'file_name' : obj.name , 'time_stamp': str(datetime.datetime.now())}
        log(log_record,'files-log.json',1)
        return HttpResponseRedirect("/"+str(id)+"/getFileDetail/")
    context["form"] = form
    return render(request, "upload.html", context)

def showMyGroup(request):
    user = request.user 
    myGroups = user.g_set.all()
    #log action
    log_record = {'user': request.user.username  , 'method' : 'showMyGroups' , 'group_name' : None , 'time_stamp': str(datetime.datetime.now())}
    log(log_record, 'groups-log.json', 4)
    return render(request , 'showMyGroup.html' , {'user': user, 'groups': myGroups})
    
def createGroup(request):
    user =request.user
    if request.method == 'POST':
        Groupname = request.POST['name']      
        Groupname = Groupname.replace(" ", "_")
        users = request.POST.getlist('users')
        users = CustomUser.objects.filter(username__in = users )
        g= G(name = Groupname  , owner= user)
        try:
            g.save()
        except Exception as e:
            return JsonResponse({"status":"fail","message":"Error!"})
        g.users.add(*users , user)
        #log action
        log_record = {'user': request.user.username  , 'method' : 'createGroup' , 'group_name' : Groupname , 'time_stamp': str(datetime.datetime.now())}
        log(log_record, 'groups-log.json', 2)
        return HttpResponseRedirect('/showMyGroups/')
    else:
        users = CustomUser.objects.all().exclude(pk  = user.pk)
        return render(request , 'CreateGroup.html'  , {'users': users})

# def editGroup(request , id):
#     user = request.user 
#     if request.method == "POST" : 
#         g = G.objects.get(pk = id )
#         g.name = request.POST['name']
#         try:
#             g.save()
#         except:
#             return JsonResponse({'status':'fail','message':'error'},status = 500)
#         g.users.remove(*g.users.all())
#         users = request.POST.getlist('users')
#         users = CustomUser.objects.filter(username__in = users )
#         g.users.add(*users , user )
#         #log action
#         log_record = {'user': request.user.username  , 'method' : 'editGroup' , 'group_name' : g.name , 'time_stamp': str(datetime.datetime.now())}
#         log(log_record, 'groups-log.json', 2)
#         return redirect('/'+str(id)+'/editGroup')
#     else:
#         g = G.objects.get(pk = id )
#         name = g.name
#         users = g.users.all()
#         restUSers = CustomUser.objects.all().exclude(pk__in = users)
#         # here is my edits 
#         blockedFilesInGroup = g.file_set.filter(~Q(block =  None))
#         result = []
#         for file in blockedFilesInGroup:
#             result.append(file.block)
#         users = users.filter(~Q(username = result))
#         return render(request ,  'editGroup.html' , {'name': name , 'users': result , 'restUSers': restUSers})
def editGroup(request , id):
    user = request.user 
    if request.method == "POST" : 
        g = G.objects.get(pk = id )
        g.name = request.POST['name']
        try:
            g.save()
        except:
            return JsonResponse({'status':'fail','message':'error'},status = 500)
        blockedFiles = g.file_set.all().filter(~Q(block = None))
        g.users.remove(*g.users.all())
        users = request.POST.getlist('users')
        users = CustomUser.objects.filter(username__in = users )
        g.users.add(*users , user )
        #log action
        log_record = {'user': request.user.username  , 'method' : 'editGroup' , 'group_name' : g.name , 'time_stamp': str(datetime.datetime.now())}
        log(log_record, 'groups-log.json', 2)
        return redirect('/'+str(id)+'/editGroup')
    else:
        g = G.objects.get(pk = id )
        name = g.name
        blockedFiles = g.file_set.all().filter(~Q(block = None))
        allUsersInGroup = g.users.all()
        restUSers = CustomUser.objects.all().exclude(pk__in = allUsersInGroup)
        allUsersInGroup = allUsersInGroup.exclude(pk = user.pk)
        usersCouldRemove = [] 
        for user in allUsersInGroup:
            if blockedFiles.filter(block = user).count() == 0 :
                usersCouldRemove.append(user)
        return render(request ,  'editGroup.html' , {'name': name , 'users': usersCouldRemove , 'restUSers': restUSers})



# dont forget to auth onwer of group only can do this 
def editGroupRemoveMember(request,  id ):
    user = request.user 
    if request.method =='POST':
        g = G.objects.all().get(pk = id )
        usersCouldNotRemove  = g.file_set.all().filter(~Q(block = None )).values_list('block' , flat = True)
        usersCouldRemove  = g.users.all().exclude(pk__in  = usersCouldNotRemove).exclude(pk = request.user.pk) 
        removedUsersList = request.POST.getlist('users')
        if usersCouldNotRemove.filter(name__in = removedUsersList).count() > 0 :
            return JsonResponse({'status':'fail','message':'error'},status = 500)

        removedUsers = usersCouldRemove.filter(username__in = removedUsersList).distinct()
        g.users.remove(*removedUsers)
        return JsonResponse({'status':'success','message':'Success'},status = 200)
        # dont forget to record log 
    else:
        g = G.objects.all().get(pk = id )
        usersCouldNotRemove  = g.file_set.all().filter(~Q(block = None )).values_list('block' , flat = True)
        usersCouldRemove  = g.users.all().exclude(pk__in  = usersCouldNotRemove).exclude(pk = request.user.pk) 
        return render (request , 'editGroupRemoveMember.html' , {'users':usersCouldRemove} )

# dont forget to auth onwer of group only can do this 
def editGroupAddMember(request, id ):
    user = request.user 
    if request.method =='POST':
        g = G.objects.get(pk = id )
        users = request.POST.getlist('users')
        users = CustomUser.objects.filter(username__in = users ).distinct()
        g.users.add(*users)
        return JsonResponse({'status':'success','message':'Success'},status = 200)
    else:
        g = G.objects.get(pk = id )
        usersCouldAdd = CustomUser.objects.all().exclude(pk__in = g.users.all()).distinct()
        return render (request , 'editGroupRemoveMember.html' , {'users':usersCouldAdd} )

    
def blockFile(request):
    user = request.user 
    if request.method == 'POST':
        files = File.objects.all().filter(name__in = request.POST.getlist('files'))
        try:
            with transaction.atomic():
                for file in files:
                    if file.block is None:
                        file.block = user
                        file.save()
                        #log action
                        log_record = {'user': request.user.username  , 'method' : 'blockFile' , 'file_name' : file.name , 'time_stamp': str(datetime.datetime.now())}
                        log(log_record, 'files-log.json', 2)
                    else:
                        1/0
        except:
            return JsonResponse({'status':'fail','message':'operation failed'})     
        return JsonResponse({'status':'success','message':'files blocked successfully'})
    
    mygroups = user.g_set.all()
    i = 0
    result = G.objects.none()
    while i< len(mygroups):
        result = list(chain(mygroups[i].file_set.all() , result))
        i = i+1 
    result = set(result)
    return render( request, 'blockFile.html' , {'files': result})

def unblockFile(request):
    user = request.user
    if request.method == 'POST':
        files = File.objects.all().filter(name__in = request.POST.getlist('files'))
        for file in files:
            file.block = None
            file.save()
            #log action
            log_record = {'user': request.user.username  , 'method' : 'unblockFile' , 'file_name' : file.name , 'time_stamp': str(datetime.datetime.now())}
            log(log_record, 'files-log.json', 2)
        return JsonResponse({'status':'success','message':'files unBlocked successfully'})
    files = File.objects.all().filter(block = user )
    return render( request, 'unblockFile.html' , {'files': files})










def testTransaction(request):
    emad = CustomUser.objects.all()[0]
    try:
        with transaction.atomic():
            emad.username = 'emad'
            emad.save()
            # a = 1/0 
    except Exception as e:
        return  HttpResponse(e)
    
    return HttpResponse(emad.username)
        




def deleteGroup(request , id ):
    try:
        deletedGroup = G.objects.all().get(id = id )
        files = File.objects.all().filter(groups = deletedGroup)
        for file in files:
            if file.block is not None:
                return JsonResponse({'status':'fail','message':'you cannot deleted this group because there is blocked file '})
            
        deletedGroup.delete()
        return JsonResponse({'status':'success','message':'group deleted'})
    except Exception as e:
        return JsonResponse({'status':'fail','message':e})
        




def reports(request):
    user = request.user 
    json_file = open(SITE_ROOT+'/media/files-log.json'  , "r")
    jsonObjs = json.load(json_file)
    results = []
    for obj in jsonObjs:
        if obj['user'] == user.username:
            results.append(obj)
    return render(request,'reports.html' , {'reports': results})





