from django.urls import path
from . import views

urlpatterns = [
    #path('', views.index, name='index'),
    path('', views.SearchSubmitView, name='index'),
    #path('search/', views.search, name='search'),
    ]