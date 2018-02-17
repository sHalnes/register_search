from django.shortcuts import render
from .models import SearchResults
from .brreg_API import find_organization


def index(request):
    data = find_organization('912660680')
    return render(request, 'index.html',context={'data': data})