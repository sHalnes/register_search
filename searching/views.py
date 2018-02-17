from django.shortcuts import render
from .models import SearchResults
from .brreg_API import find_organization


def index(request):
    org_num = '000'
#    org_num = '912660680'

    data = find_organization(org_num)
    if not data:
        data = 'Foretak med organisasjosnummeret {} er ikke registrert'.format(org_num)
    return render(request, 'index.html',context={'data': data})