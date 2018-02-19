from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search, name='search'),
    path('orgview/', views.orgview, name='orgview'),
    path('links/', views.links, name='links'),
    path('map/', views.map, name='map'),
    ]