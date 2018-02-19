import json
import requests

def get_geodata(address):
    '''
    Find and return lattitude and longitude to the first matching address from geonorge API
    :param address: (street, building, postnumber, poststed, kommunenumber, kommune)
    :return: float lat, lon
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
            return 0
    return lat, lon

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
            return lat, lon
    return 0



#get_geodata('Haldenveien', '67', 'ringerike')
#address = ('Havnegata','48','8900', 'BRØNNØYSUND','1813', 'BRØNNØY')
#a,b = get_geodata(address)

'''

{'sokStatus': {'ok': 'true', 'melding': ''},
'totaltAntallTreff': '37453', 'adresser':
[{'type': 'Vegadresse',
'adressekode': '8000',
'adressenavn': 'Haldenveien',
'kortadressenavn': 'Haldenveien',
'husnr': '67',
'undernr': '0',
'postnr': '3515',
'poststed': 'HØNEFOSS',
'kommunenr': '0605',
 'kommunenavn': 'RINGERIKE',
 'gardsnr': '87',
 'bruksnr': '321',
 'festenr': '0',
 'seksjonsnr': '0',
 'bruksnavn': 'FLATA',
 'nord': '60.18321133466702',
 'aust': '10.254246883657563'



'adresse': 'Havnegata 48',
    'postnummer': '8900',
    'poststed': 'BRØNNØYSUND',
    'kommunenummer': '1813',
    'kommune': 'BRØNNØY',

http://ws.geonorge.no/AdresseWS/adresse/sok?sokestreng=Haldenveien%2067,ringerike

'''