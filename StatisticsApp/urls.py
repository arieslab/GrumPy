from django.urls import path

from . import views

urlpatterns = [
    path('', views.statistics_index, name='statistics_index'),

]