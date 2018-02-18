from django.shortcuts import render
from .models import SearchResults
from .brreg_API import find_organization

from django.views.generic.base import View
from django.http import HttpResponse
from django.template import loader



def index(request):
    response_message = 'This is the response from index'
    query = request.POST.get('search', '')
    data = []
    reg_num = False
    # a simple query. not sure I need it here
    #if len(query) > 2:
     #   reg_num, data = find_organization(query)

    return render(request, 'index.html', context={'title':response_message, 'data': data, 'reg_num':reg_num})

def search(request):
    response_message = ''
    query = request.POST.get('search', '')
    data = []
    reg_num = False
    # we begin search as soon as number of letters is bigger than 2
    if len(query) > 2:
        reg_num, data = find_organization(query)
    # in case we cannot find data about reg number or organization's name
    if (len(query) == 9 and query.isnumeric() and data == 0) or (len(query) > 2 and not query.isnumeric() and data == 0):
        response_message = "Ingen treff"
    elif len(query) > 9 and query.isnumeric():
        response_message = "Feil reg. nummer"
    # print out number of results
    elif len(query) > 2 and not query.isnumeric():
        response_message = "Det finnes " + str(len(data)) + " treff: "
    # if user try to search special symbols
    #elif len(query) > 2 and not query.isnumeric() and not query.isalpha() and data == 0:
    #    response_message = "Er du sikker dette er et riktig navn?"

    context = {'message':response_message, 'query':query, 'data':data, 'reg_num': reg_num}
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