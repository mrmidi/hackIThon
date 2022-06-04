from django.urls import path
from . import views
#from dash_apps import activity

urlpatterns = [
    path('', views.activity, name='activity'),
    path('activity/', views.activity, name='activity')
]
