# -*- coding: utf-8 -*-
#SECRET_KEY = "@zudr3e%^%=(5noc-z0y^p9^8&mhtnci@3+&ipleqfavsu1)bj"


'''

<li> {{ x2 }} med organisasjonsnummeret {{ x1 }}</li>

                 <li><a href="{% url 'search' x1 %}">{{ x2 }}</a></li>







<form id="form" role="form" action="{% url 'index' %}" method="post">
    {% csrf_token %}
    <input name="search"
           type="search"
           id="search"
           placeholder="Tast inn regnum eller navn"
           ic-post-to="{% url 'search' %}"
           ic-trigger-on="keyup changed"
           ic-trigger-delay="30ms"
           ic-target="#search-result-container"
    />
    <!--button type="submit">SøK!</button-->
</form>
<form name="search" method="post" action="{% url 'index' %}">
        {% csrf_token %}
    <input type="hidden" name="supporttype" id="search"/>
    <input type="submit" value="{{ org_num }}" />
</form>
<button type="submit">{{ name }}</button>






{% if data.count > 1 %}

{% for element in data %}

<li> {{ element}}</a></li>

{% endfor %}

{% else %}

<li>Ingenting å vise</li>

{% endif %}'''


import json
import requests


def find_organization(input_string):
    '''
    Find and return data from bberg API
    :param input_string: a string with length >= 3. If the length == 9 and consists of numbers: the string is org. number. Else: it can be or it is a org. name.
    :return: data if exist, zero if there is no data
    '''
    #http://data.brreg.no/enhetsregisteret/enhet.{format}?page = {side} & size = {antall per side} & $filter = {filter}
    #http://data.brreg.no/enhetsregisteret/enhet/{orgnr}.{format}
    #http://data.brreg.no/enhetsregisteret/underenhet/{organisasjonsnummer}.{format}
    #'http://data.brreg.no/enhetsregisteret/underenhet/874714852.json'  #
    #http://data.brreg.no/enhetsregisteret/underenhet/874714852.json
    data_to_return = []
    url_enhet = 'http://data.brreg.no/enhetsregisteret/enhet'
    url_underenhet = 'http://data.brreg.no/enhetsregisteret/underenhet'
    if len(input_string) == 9 and input_string.isnumeric():
        #url = 'http://data.brreg.no/enhetsregisteret/enhet'
        request_url = (url_enhet + '/{}.json').format(input_string)
        response = requests.get(request_url)
        # looking for enhet or underenhet
        if response.status_code == 200:
            try:
                raw_data = json.loads(response.text)
                #print(raw_data)
                data_to_return = get_data_from_jsson(raw_data)
            except(ValueError, KeyError, TypeError):
                #print('something went wrong')
                return 0
        else:
            #url = 'http://data.brreg.no/enhetsregisteret/underenhet'
            request_url = (url_underenhet + '/{}.json').format(input_string)
            response = requests.get(request_url)
            if response.status_code == 200:
                try:
                    raw_data = json.loads(response.text)
                    #print(raw_data)
                    data_to_return = get_data_from_jsson(raw_data)
                except(ValueError, KeyError, TypeError):
                    #print('something went wrong')
                    return 0
    #$filter=startswith(navn,'Brønnøy')
    #http://data.brreg.no/enhetsregisteret/enhet.{format}?page = {side} & size = {antall per side} & $filter = {filter}
    #http://data.brreg.no/enhetsregisteret/underenhet.{format}?page = {side} & size = {antall per side} & $filter = {filter}
# http://data.brreg.no/enhetsregisteret/enhet.json?$filter=startswith%28navn%2C%27Brønnøy%27%29
    #http://data.brreg.no/enhetsregisteret/enhet.json?$filter = startswith(navn,'Brønnøy')

    # here we need to return results for both enhets and underenhets
    # if the given name written with norwegian letters,
    elif len(input_string) > 2 and not input_string.isnumeric():
        input_string = input_string.upper()
        #checking enhet
        #request_url = (url_enhet + '.json?$filter=startswith%28navn%2C%27{}%27%29').format(input_string)
        #request_url = 'http://data.brreg.no/enhetsregisteret/enhet.json?$filter=startswith%28navn%2C%27Brønnøy%27%29'
        request_url = 'http://data.brreg.no/enhetsregisteret/enhet.json?$filter=startswith%28navn%2C%27'+input_string+'%27%29'
        response = requests.get(request_url)
        print(response.status_code)
        if response.status_code == 200:
            try:
                raw_data = json.loads(response.text)
                print(raw_data)
                data_to_return = cont_search_data(raw_data)
                print(data_to_return)
            except(ValueError, KeyError, TypeError):
                print('something went wrong')
                return 0
        # # checking underenhet
        # request_url = 'http://data.brreg.no/enhetsregisteret/underenhet.json?$filter=startswith%28navn%2C%27'+input_string+'%27%29'
        # response = requests.get(request_url)
        # if response.status_code == 200:
        #     try:
        #         raw_data = json.loads(response.text)
        #         print(raw_data)
        #         data_to_return = cont_search_data(raw_data)
        #         print(data_to_return)
        #     except(ValueError, KeyError, TypeError):
        #         print('something went wrong')
        #         return 0

    #print(data_to_return)
    return data_to_return


def cont_search_data(raw_data):
    data_to_return = []
    print('len of len(raw_data[data])', len(raw_data['data']))
    for el in range(len(raw_data['data'])):
        print(el, raw_data['data'][el]['organisasjonsnummer'])
        data_to_return.append([raw_data['data'][el]['organisasjonsnummer'], raw_data['data'][el]['navn']])
    return data_to_return

#"data":[
#      {
#         "organisasjonsnummer":990490813,
#         "navn":"KOMMUNEKASSERAREN I LEIKANGER",

def get_data_from_jsson(raw_data):
    '''
    Function to get and format data from json
    :param raw_data: raw data
    :return: list with data
    '''
    data_to_return = []

    json_keys = {
        'organisasjonsnummer':['organisasjonsnummer'],
        'navn':['navn'],
        'registreringsdatoEnhetsregisteret':['registreringsdatoEnhetsregisteret'],
        'antallAnsatte':['antallAnsatte'],
        'hjemmeside':['hjemmeside'],
        'orgform':['orgform', 'beskrivelse'],
        'naeringskode1':['naeringskode1', 'beskrivelse'],
        'postadresse':['postadresse', 'adresse', 'postnummer', 'poststed'],
        'beliggenhetsadresse':['beliggenhetsadresse', 'adresse', 'postnummer', 'poststed'],
        'forretningsadresse': ['forretningsadresse', 'adresse', 'postnummer', 'poststed'],
        'konkurs': ['konkurs']
        }
    keys_description = {
        'organisasjonsnummer':'Organisasjonsnummer: ',
        'navn':'Navn: ',
        'registreringsdatoEnhetsregisteret': 'Registrert: ',
        'antallAnsatte': 'Antall ansatte: ',
        'hjemmeside': 'Hjemmeside: ',
        'orgform': 'Organisasjonsform: ',
        'naeringskode1': 'Oppgave: ',
        'postadresse': 'Postadresse: ',
        'beliggenhetsadresse': 'Beliggenhet: ',
        'forretningsadresse': 'Beliggenhet: ',
        'konkurs': 'Konkurs: '
    }

    # retrieve data from raw json
    for key in json_keys:
        #print(key)
        if key in raw_data and key in keys_description:
            data_str = ''
            data_str += keys_description[key]
            if len(json_keys[key]) > 1:
                for underkey in range(1, len(json_keys[key])):
                    if json_keys[key][underkey] in raw_data[key]:
                        data_str += str(raw_data[key][json_keys[key][underkey]])+' '
                        #data_to_return.append(raw_data[key][json_keys[key][underkey]])
                        #print(raw_data[key][json_keys[key][underkey]])
            else:
                data_str += str(raw_data[key])
                #data_to_return.append(raw_data[key])
                #print(raw_data[key])
            data_to_return.append(data_str)

    return data_to_return


#print('underenhet')
#find_organization('874714852')
#print('\nenhet')
#find_organization('974760673')
#print('\nenhet')
#find_organization('912660680')
find_organization('Kartverket')

#find_organization('Brønnøy')
#find_organization('NULL')


