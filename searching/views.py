from django.shortcuts import render
from .brreg_API import find_organization
from .kartverket_API import get_geodata
from django.http import HttpResponse

# this was a try to implement map

def index(request):
    response_message = 'This is the response from index'
    query = request.POST.get('search', '')
    data = []
    reg_num = False
    # a simple query. not sure I need it here
    reg_num, data = find_organization(query)
#    reg_num, data, adresse = find_organization(query)

    if len(query) > 2:
        reg_num, data = find_organization(query)
    #        reg_num, data, adresse = find_organization(query)
    # in case we cannot find data about reg number or organization's name
    if (len(query) == 9 and query.isnumeric() and data == 0) or (
            len(query) > 2 and not query.isnumeric() and data == 0):
        response_message = "Ingen treff"
    elif len(query) > 9 and query.isnumeric():
        response_message = "Feil reg. nummer"
    # print out number of results
    elif len(query) > 2 and not query.isnumeric():
        response_message = "Det finnes " + str(len(data)) + " treff: "
    context = {'message': response_message, 'query': query, 'data': data, 'reg_num': reg_num}
    rendered_template = render(request, 'index.html', context)
    return HttpResponse(rendered_template, content_type='text/html')


    #return render(request, 'index.html', context={'title':response_message, 'data': data, 'reg_num':reg_num})

def search(request):
    response_message = ''
    query = request.POST.get('search', '')
    data = []
    reg_num = False
    # we begin search as soon as number of letters is bigger than 2
    if len(query) > 2:
        reg_num, data = find_organization(query)
#        reg_num, data, adresse = find_organization(query)
    # in case we cannot find data about reg number or organization's name
    if (len(query) == 9 and query.isnumeric() and data == 0) or (len(query) > 2 and not query.isnumeric() and data == 0):
        response_message = "Ingen treff"
    elif len(query) > 9 and query.isnumeric():
        response_message = "Feil reg. nummer"
    # print out number of results
    elif len(query) > 2 and not query.isnumeric():
        response_message = "Det finnes " + str(len(data)) + " treff: "
    context = {'message':response_message, 'query':query, 'data':data, 'reg_num': reg_num}
    rendered_template = render(request, 'search.html',context)
    return HttpResponse(rendered_template, content_type='text/html')


def orgview(request):
    '''
    This function calls only when user choose a company from interactive search. An ugly solution which works.
    :param request: reg number
    :return: HTTP response with data from API about the company.
    '''
    response_message = ''
    query = request.POST.get('search', '')
#    reg_num, data, adresse = find_organization(query)
    reg_num, data = find_organization(query)
    context = {'message':response_message, 'query':query, 'data':data, 'reg_num': reg_num}
    rendered_template = render(request, 'orgview.html',context)
    return HttpResponse(rendered_template, content_type='text/html')


def links(request):
    rendered_template = render(request, 'links.html',context={})
    return HttpResponse(rendered_template, content_type='text/html')

def map(request):
    #if len(lat_lon) > 0:
    #    lat, lon = get_geodata(adresse)
    #    context = {'latlon': (float(lat), float(lon))}
    #else:
    context = {}
    # address = ('Havnegata','48','8900', 'BRØNNØYSUND','1813', 'BRØNNØY')
    # lat, lon = get_geodata(address)
    # context = {'latlon':(float(lat), float(lon))}
    rendered_template = render(request, 'map.html',context)
    return HttpResponse(rendered_template, content_type='text/html')

