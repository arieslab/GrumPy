from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('keys', views.keyList, name='key'),
    path('keyform', views.newKey, name='keyform')
]