import json
import requests


def find_organization(input_string):
    '''
    Find and return data from bberg API
    :param input_string: a string with length >= 3. If the length == 9 and consists of numbers: the string is org. number. Else: it can be or it is a org. name.
    :return: data if exist, empty string if there is no data
    '''
    #http://data.brreg.no/enhetsregisteret/enhet.{format}?page = {side} & size = {antall per side} & $filter = {filter}
    #http://data.brreg.no/enhetsregisteret/enhet/{orgnr}.{format}
    #http://data.brreg.no/enhetsregisteret/underenhet/{organisasjonsnummer}.{format}
    #'http://data.brreg.no/enhetsregisteret/underenhet/874714852.json'  #
    #http://data.brreg.no/enhetsregisteret/underenhet/874714852.json
    url = 'http://data.brreg.no/enhetsregisteret/enhet'
    if len(input_string) == 9 and input_string.isnumeric():
        request_url = (url + '/{}.json').format(input_string)
        response = requests.get(request_url)#(url, data=request_url)
        # looking for enhet or underenhet
        if response.status_code == 200:
            try:
                raw_data = json.loads(response.text)
                #print(raw_data)
                get_data_from_jsson(raw_data)
            except(ValueError, KeyError, TypeError):
                print('WRONG!')
                return 0
        else:
            url = 'http://data.brreg.no/enhetsregisteret/underenhet'
            request_url = (url + '/{}.json').format(input_string)
            response = requests.get(request_url)
            if response.status_code == 200:
                try:
                    raw_data = json.loads(response.text)
                    #print(raw_data)
                    get_data_from_jsson(raw_data)
                except(ValueError, KeyError, TypeError):
                    print('WRONG!')
                    return 0

            #print('no answer')
            #return 'Foretak med organisasjosnummeret {} er ikke registrert'.format(input_string)

def get_data_from_jsson(raw_data):
    '''
    Function to get and format data from json
    :param raw_data: raw data
    :return:
    '''
    # here enhet and underenhet may have different fields, so in this case I think we can use dictionary to get information from json
    json_keys_common = {
        'organisasjonsnummer':['organisasjonsnummer'],
        'navn':['navn'],
        'registreringsdatoEnhetsregisteret':['registreringsdatoEnhetsregisteret'],
        'antallAnsatte':['antallAnsatte'],
        'hjemmeside':['hjemmeside'],
        'orgform':['orgform', 'beskrivelse'],
        'naeringskode1':['naeringskode1', 'beskrivelse'],
        'postadresse':['postadresse', 'adresse', 'postnummer', 'poststed'],
        'beliggenhetsadresse':['beliggenhetsadresse', 'adresse', 'postnummer', 'poststed'],
        # just test it works without another dict
        'forretningsadresse': ['forretningsadresse', 'adresse', 'postnummer', 'poststed'],
        'konkurs': ['konkurs']
        }
    # if json has 'institusjonellSektorkode'
    # json_keys_enhet = {
    #     'beskrivelse':['beskrivelse'],
    #     'naeringskode1': ['naeringskode1', 'beskrivelse'],
    #     'postadresse': ['postadresse', 'adresse', 'postnummer', 'poststed'],
    #     'forretningsadresse': ['forretningsadresse', 'adresse', 'postnummer', 'poststed'],
    #     'konkurs':['konkurs']
    # }

    # retrieve data from raw json
    for key in json_keys_common:
        if key in raw_data:
            print(key)
            if len(json_keys_common[key]) > 1:
                for underkey in range(1, len(json_keys_common[key])):
                    if json_keys_common[key][underkey] in raw_data[key]:
                        print(raw_data[key][json_keys_common[key][underkey]])
            else:
                print(raw_data[key])

    # if enhet with 'institusjonellSektorkode'
    # if 'institusjonellSektorkode' in raw_data:
    #     for key in json_keys_enhet:
    #         if key in raw_data['institusjonellSektorkode']:
    #             print(key)
    #             if len(json_keys_enhet[key]) > 1:
    #                 for underkey in range(1, len(json_keys_enhet[key])):
    #                     if json_keys_enhet[key][underkey] in raw_data['institusjonellSektorkode'][key]:
    #                     #if raw_data['institusjonellSektorkode'][json_keys_enhet[key][underkey]]:
    #                         print(raw_data['institusjonellSektorkode'][json_keys_enhet[key][underkey]])
    #             else:
    #                 print(raw_data['institusjonellSektorkode'][key])


print('underenhet')
find_organization('874714852')
print('\nenhet')
find_organization('974760673')
print('\nenhet')
find_organization('912660680')
