from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('keys', views.keyList, name='key'),
    path('teste', views.teste),
    path('detailed_issue', views.detailed_issue, name="detailed_issue"),
    path('issues', views.issues, name="issues"),
    path('keyform', views.newKey, name='keyform'),
    path('deletekey/<int:id>', views.deleteKey, name="deletekey"),
    path('miners', views.index, name='miners'),
    path('minerform', views.newMiner, name='minerform'),
    path('startmining/<int:id>', views.startMining, name="startmining"),
    path('stopmining/<int:id>', views.stopMining, name="stopmining"),
    path('deleteminer/<int:id>', views.deleteMiner, name="deleteminer"),
    path('viewprogress/<int:id>', views.viewprogress, name='viewprogress'),
    path('statisticsMain', views.MainStatistics, name='statisticsMain'),
]