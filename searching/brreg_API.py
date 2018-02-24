# -*- coding: utf-8 -*-
#import json
#import requests
#from . import kartverket_API


import json
import requests

def get_geodata(address):
    '''
    Find and return lattitude and longitude to the first matching address from geonorge API
    :param address: (street, building, postnumber, poststed, kommunenumber, kommune)
    :return: float lat, lon, or (-1,-1) if the coords cannot be found
    '''
    street, building, postnumber, poststed, kommunenumber, kommune = address
    lat = lon = '0.0'
    url = 'http://ws.geonorge.no/AdresseWS/adresse/sok?sokestreng={}%20{},{}'.format(street,building,kommune.lower())
    response = requests.get(url)
    if response.status_code == 200:
        try:
            raw_data = json.loads(response.text)
            lat, lon = find_coords(raw_data,address)
        except(ValueError, KeyError, TypeError):
            return (-1,-1)
    return (float(lat), float(lon))

def find_coords(raw_data, address):
    street, building, postnumber, poststed, kommunenumber, kommune = address
    for i in range(len(raw_data['adresser'])):
        if (raw_data['adresser'][i]['adressenavn'] == street and
                raw_data['adresser'][i]['husnr'] == building and
                raw_data['adresser'][i]['postnr'] == postnumber and
                raw_data['adresser'][i]['poststed'] == poststed and
                raw_data['adresser'][i]['kommunenr'] == kommunenumber and
                raw_data['adresser'][i]['kommunenavn'] == kommune):
            lat = raw_data['adresser'][i]['nord']
            lon = raw_data['adresser'][i]['aust']
            return (lat, lon)
    return (-1,-1)







def find_organization(input_string):
    '''
    Find and return data from bberg API
    :param input_string: a string with length >= 3. If the length == 9 and consists of numbers: the string is org. number. Else: it can be or it is a org. name.
    :return: data if exist, zero if there is no data + a boolean variable to describe kind of data
    '''
    data_to_return = []
    #address = ()
    lat_lon = (-1,-1)
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
            except Exception as inst:
                print(type(inst))  # the exception instance
                print(inst.args)  # arguments stored in .args
                print(inst)
            # except(ValueError, KeyError, TypeError):
            #     print()
            #     print('something went wrong')
            #     data_to_return = 0
        else:
            request_url = (url_underenhet + '/{}.json').format(input_string)
            response = requests.get(request_url)
            if response.status_code == 200:
                try:
                    raw_data = json.loads(response.text)
                    data_to_return, lat_lon = get_data_from_jsson(raw_data)
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
    return (reg_num, data_to_return, lat_lon)
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
        'beliggenhetsadresse':['beliggenhetsadresse', 'adresse', 'postnummer', 'poststed', 'land'],
        'forretningsadresse': ['forretningsadresse', 'adresse', 'postnummer', 'poststed', 'land'],
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

# here we need to be careful with land code. if the land code is not NO and land is not Norway, we should not even try to find coordinates
    land = ''
    lat_lon = (-1, -1) # default value for coordinates if land != 'Norge'

    # retrieve data from raw json
    for key in json_keys:
        if key in raw_data and key in keys_description:

            if key == 'konkurs' and raw_data[key] == 'J':
                data_to_return.append(raw_data[key])
            elif key != 'konkurs':
                data_str = ''
                data_str += keys_description[key]
                if len(json_keys[key]) > 1:
                    for underkey in range(1, len(json_keys[key])):
                        #sprint(underkey)
                        #if raw_data[key][json_keys[key][underkey]]:
                        if json_keys[key][underkey] in raw_data[key]:
                            data_str += str(raw_data[key][json_keys[key][underkey]])+' '
                            if json_keys[key][underkey] == 'land' and raw_data[key][json_keys[key][underkey]] == 'Norge':
                                land = 'Norge'
                        #else:
                        #    print('there is no element', json_keys[key][underkey])
                else:
                    data_str += str(raw_data[key])
                data_to_return.append(data_str)
    #trying to get address
    if land == 'Norge':
        address_keys = ['adresse', 'postnummer', 'poststed', 'kommunenummer', 'kommune']
        address = []
        if 'beliggenhetsadresse' in raw_data:
            for element in address_keys:
                if raw_data['beliggenhetsadresse'][element]:
                    address.append(raw_data['beliggenhetsadresse'][element])
        elif 'forretningsadresse' in raw_data:
            for element in address_keys:
                if raw_data['forretningsadresse'][element]:
                    address.append(raw_data['forretningsadresse'][element])

        # if there are less data to find coords, else will come to the picture
        #print('length of address: ', len(address))
        if len(address) == 5:
            #print('address == 6 so we trying to find coords')
            street_data = address[0].split()
            street = ' '.join(street_data[:-1])
            building = street_data[-1]
            postnummer = address[1]
            poststed = address[2]
            kommunenummer = address[3]
            kommune = address[4]
            addresse = (street, building, postnummer, poststed, kommunenummer, kommune)
            lat_lon = get_geodata(addresse)
    #else:
    #    print('this is not in Norway')
    #print(data_to_return)
    #print('lat lon',lat_lon)
    return data_to_return, lat_lon

#address = ('Havnegata','48','8900', 'BRØNNØYSUND','1813', 'BRØNNØY')

test_cases = ['988997072','918837078', '919767553','990256039','990873739','987740353']
for test in test_cases:
    a,b,c = find_organization(test)
    print(test,a, b,c, end='\n\n')


#find_organization('988997072')
#find_organization('918837078')