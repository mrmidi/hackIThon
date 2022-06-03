from django.urls import path
from . import views
#from dash_apps import activity

urlpatterns = [
    path('', views.blank, name='hello_world'),
    path('activity/', views.activity, name='activity')
]
