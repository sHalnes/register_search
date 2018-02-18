from django.urls import path
#from searching.views import SearchSubmitView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    #path('', SearchSubmitView.as_view()),
    path('search/', views.search, name='search'),
    path('orgview/', views.orgview, name='orgview')
    ]