from django.shortcuts import render
from .models import SearchResults
from .brreg_API import find_organization


def index(request):
    if request.method == 'POST':
        search_text = request.POST['search_text']
    else:
        search_text = ''
#    org_num = 'Kart'
#    org_num = '912660680'

    data = find_organization(search_text)
    if not data:
        data = ['Foretak med organisasjosnummeret {} er ikke registrert'.format(search_text)]
    #return render(request, 'search.html', context={'data':data})
    return render(request, 'index.html',context={'data': data})

def search(request):
    pass