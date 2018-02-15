from django.shortcuts import render
from .models import SearchResults


def index(request):
    data = ['first', 'second']
    return render(request, 'index.html',context={'data': data})