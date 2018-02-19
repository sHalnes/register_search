# -*- coding: utf-8 -*-
import json
import requests

def find_organization(input_string):
    '''
    Find and return data from bberg API
    :param input_string: a string with length >= 3. If the length == 9 and consists of numbers: the string is org. number. Else: it can be or it is a org. name.
    :return: data if exist, zero if there is no data + a boolean variable to describe kind of data
    '''
    data_to_return = []
    address = ()
    reg_num = False
    url_enhet = 'http://data.brreg.no/enhetsregisteret/enhet'
    url_underenhet = 'http://data.brreg.no/enhetsregisteret/underenhet'
    if len(input_string) == 9 and input_string.isnumeric():
        reg_num = True
        request_url = (url_enhet + '/{}.json').format(input_string)
        response = requests.get(request_url)
        # looking for enhet or underenhet
        if response.status_code == 200:
            try:
                raw_data = json.loads(response.text)
                data_to_return = get_data_from_jsson(raw_data)
            except(ValueError, KeyError, TypeError):
                data_to_return = 0
        else:
            request_url = (url_underenhet + '/{}.json').format(input_string)
            response = requests.get(request_url)
            if response.status_code == 200:
                try:
                    raw_data = json.loads(response.text)
                    data_to_return = get_data_from_jsson(raw_data)
                except(ValueError, KeyError, TypeError):
                    data_to_return = 0
            else:
                data_to_return = 0
    # here we need to return results for both enhets and underenhets
    # if the given name written with norwegian letters,
    elif len(input_string) > 2 and not input_string.isnumeric():
        input_string = input_string.upper()
        #checking enhet. This strange link means I did not succseed with a standart link $filter = {filter}
        request_url = 'http://data.brreg.no/enhetsregisteret/enhet.json?$filter=startswith%28navn%2C%27'+input_string+'%27%29'
        response = requests.get(request_url)
        if response.status_code == 200:
            try:
                raw_data = json.loads(response.text)
                data_to_return = cont_search_data(raw_data)
            except(ValueError, KeyError, TypeError):
                data_to_return = 0
        else:
            data_to_return = 0
    return (reg_num, data_to_return)
#    return (reg_num, data_to_return, address)


def cont_search_data(raw_data):
    """
    Function for interactive search. Returns organization number and name if partial name is matches
    :param raw_data: json data filtred by first letters
    :return: list
    """
    data_to_return = []
    for el in range(len(raw_data['data'])):
        data_to_return.append([raw_data['data'][el]['organisasjonsnummer'], raw_data['data'][el]['navn']])
    return data_to_return



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
        'konkurs': '' #'Konkurs: '
    }

    #address_keys = ['adresse', 'postnummer', 'poststed', 'kommunenummer', 'kommune']
    #address = []

    # retrieve data from raw json
    for key in json_keys:
        if key in raw_data and key in keys_description:

            if key == 'konkurs' and raw_data[key] == 'J':
                data_to_return.append(raw_data[key])
                continue

            data_str = ''
            data_str += keys_description[key]
            if len(json_keys[key]) > 1:
                for underkey in range(1, len(json_keys[key])):
                    if json_keys[key][underkey] in raw_data[key]:
                        data_str += str(raw_data[key][json_keys[key][underkey]])+' '
            else:
                data_str += str(raw_data[key])
            data_to_return.append(data_str)

    # if 'beliggenhetsadresse' in raw_data:
    #     for element in address_keys:
    #         address.append(raw_data['beliggenhetsadresse'][element])
    # elif 'forretningsadresse' in raw_data:
    #     for element in address_keys:
    #         address.append(raw_data['forretningsadresse'][element])
    #
    # street_data = address[0].split()
    # street = address[0][:(len(address[0] - len(street_data[-1]-1)))]
    # building = street_data[-1]
    # postnummer = address[1]
    # poststed = address[2]
    # kommunenummer = address[3]
    # kommune = address[4]
    # address_to_return = (street, building, postnummer, poststed, kommunenummer, kommune)
    return data_to_return

#address = ('Havnegata','48','8900', 'BRØNNØYSUND','1813', 'BRØNNØY')
#print('underenhet')
#find_organization('874714852')
#print('\nenhet')
#find_organization('974760673')
#print('\nenhet')
#find_organization('912660680')
#find_organization('Kartv')

#find_organization('Br%C3%B8nn%C3%B8y')
#find_organization('Brønnøy')

