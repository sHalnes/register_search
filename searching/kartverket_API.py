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
