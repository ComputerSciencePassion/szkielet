import http.client
import json
from urllib.parse import urlencode
from .models import Atrakcja

def calculate_attraction_order(start_node_lat, start_node_lng, attractions):
    api_key = 'AIzaSyDUj5pTuHqBU3LdNXJIXlM2Gzb2IofPVAM'
    host = 'maps.googleapis.com'
    endpoint = '/maps/api/distancematrix/json'

    # Construct the parameters for the API request
    params = {
        'origins': f'{start_node_lat},{start_node_lng}',
        'destinations': '|'.join([f'{atrakcja.latitude},{atrakcja.longitude}' for atrakcja in Atrakcja.objects.filter(nazwa_atrakcji__in=attractions)]),
        'mode': 'walking',
        'key': api_key
    }

    # Create the HTTPS connection
    conn = http.client.HTTPSConnection(host)

    # Send the GET request
    conn.request('GET', f'{endpoint}?{urlencode(params)}')

    # Get the response and parse the JSON data
    response = conn.getresponse()
    data = response.read().decode('utf-8')
    json_data = json.loads(data)

    # Process the response to get the ordered attractions
    ordered_attractions = []
    if json_data['status'] == 'OK':
        rows = json_data['rows'][0]['elements']
        distances = [row['distance']['value'] for row in rows]
        sorted_attractions = sorted(zip(attractions, distances), key=lambda x: x[1])
        ordered_attractions = [attraction[0] for attraction in sorted_attractions]
    conn.close()

    return ordered_attractions
