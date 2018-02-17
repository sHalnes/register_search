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
    if len(input_string) == 9 and input_string.isnumeric():
        url = 'http://data.brreg.no/enhetsregisteret/enhet'
        request_url = (url + '/{}.json').format(input_string)
        response = requests.get(request_url)
        # looking for enhet or underenhet
        if response.status_code == 200:
            try:
                raw_data = json.loads(response.text)
                print(raw_data)
                data_to_return = get_data_from_jsson(raw_data)
            except(ValueError, KeyError, TypeError):
                print('something went wrong')
                return 0
        else:
            url = 'http://data.brreg.no/enhetsregisteret/underenhet'
            request_url = (url + '/{}.json').format(input_string)
            response = requests.get(request_url)
            if response.status_code == 200:
                try:
                    raw_data = json.loads(response.text)
                    print(raw_data)
                    data_to_return = get_data_from_jsson(raw_data)
                except(ValueError, KeyError, TypeError):
                    print('something went wrong')
                    return 0
    #print(data_to_return)
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
        'konkurs': 'Konkurs'
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
                        data_str += str(raw_data[key][json_keys[key][underkey]])
                        #data_to_return.append(raw_data[key][json_keys[key][underkey]])
                        #print(raw_data[key][json_keys[key][underkey]])
            else:
                data_str += str(raw_data[key])
                #data_to_return.append(raw_data[key])
                #print(raw_data[key])
            data_to_return.append(data_str)

    return data_to_return


#print('underenhet')
find_organization('874714852')
#print('\nenhet')
find_organization('974760673')
#print('\nenhet')
#find_organization('912660680')
