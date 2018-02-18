from django.shortcuts import render
from .models import SearchResults
from .brreg_API import find_organization

from django.views.generic.base import View
from django.http import HttpResponse
from django.template import loader



def index(request):
    response_message = 'This is the response'
    query = request.POST.get('search', '')

    # a simple query
    data = find_organization(query)

    #context = {'title':response_message, 'query':query, 'data':data}
    #rendered_template = render(request, 'index.html',context)
    #return HttpResponse(rendered_template, content_type='text/html')
    return render(request, 'index.html', context={'data': data})

def search(request):
    response_message = 'This is the Ajax response'
    query = request.POST.get('search', '')

    # a simple query
    data = find_organization(query)
    context = {'title':response_message, 'query':query, 'data':data}
    #    return render(request, 'index.html',context={'data': data})
    rendered_template = render(request, 'search.html',context)
    return HttpResponse(rendered_template, content_type='text/html')
'''
def index(request):
    if request.method == 'POST':
        search_text = request.POST['search_text']
    else:
        #search_text = ''
        search_text = 'Kart'
#    org_num = '912660680'

    data = find_organization(search_text)
    if not data:
        data = ['Foretak med organisasjosnummeret {} er ikke registrert'.format(search_text)]
    #return render(request, 'search.html', context={'data':data})
    return render(request, 'index.html',context={'data': data})

def search(request):
    if request.method == 'POST':
        search_text = request.POST['search_text']
    else:
         search_text = ''

    data = find_organization(search_text)
    if not data:
        data = ['Foretak med organisasjosnummeret {} er ikke registrert'.format(search_text)]
    return render(request, 'search.html', context={'data': data})
    
    
    
class SearchSubmitView(View):
    template = 'index.html'
    response_message = 'This is the response'

    def post(self, request):
        template = loader.get_template(self.template)
        query = request.POST.get('search', '')

        # a simple query
        data = find_organization(query)

        context = {'title':self.response_message, 'query':query, 'data':data}
        rendered_template = template.render(context, request)
        return HttpResponse(rendered_template, content_type='text/html')
'''