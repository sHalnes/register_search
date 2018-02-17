from django.urls import path
from . import views

urlpatterns = [
    #path('', views.index, name='index'),
    path('', views.SearchSubmitView.as_view(), name='index'),
    #path('search/', views.search, name='search'),
    ]