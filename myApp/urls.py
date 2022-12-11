
from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('upload/', views.upload , name='upload'),
    path('<id>/update', views.update , name='update'),
    path('<id>/delete', views.delete , name='delete'),
    path("createGroup/", views.createGroup, name="createGroup"), 
    path("<id>/getFileDetail/", views.getFileDetail, name="getFileDetail"), 
    path("<id>/getGroupDetail/", views.getGroupDetail, name="getGroupDetail"), 
    path("showMyGroups/", views.showMyGroup, name="showMyGroup"), 
    
    path("home/", views.home, name="home"), 
    path("<id>/displayContent", views.displayContent, name="displayContent"), 
    path("<id>/editContent", views.editContent, name="editContent"),
    path("<id>/editGroup", views.editGroup, name="editGroup"),
    path("blockFile/", views.blockFile, name="blockFile"),
    path("unblockFile/", views.unblockFile, name="unblockFile"),
    path("showMyFiles/", views.showMyFiles, name="showMyFiles"),

     path("", views.index, name="index"),
     path("contact/", views.contact, name="contact"),

    #path("testTransaction/", views.testTransaction, name="testTransaction"),
    path("<id>/deleteGroup", views.deleteGroup, name="deleteGroup"),
    path("reports/", views.reports, name="reports"),
    path("<id>/editGroupRemoveMember", views.editGroupRemoveMember, name="editGroupRemoveMember"),
    path("<id>/editGroupAddMember", views.editGroupAddMember, name="editGroupAddMember"),
    
]


if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)