import requests, uuid, json

# Add your subscription key and endpoint
subscription_key = "f060c48b82fc46b1b9ff0e234cb4067b"
endpoint = "https://api.cognitive.microsofttranslator.com"

# Add your location, also known as region. The default is global.
# This is required if using a Cognitive Services resource.
location = "northeurope"

path = '/translate'
constructed_url = endpoint + path

params = {
    'api-version': '3.0',
    'includeAlignment': 'true',
    'from': 'en',
    'to': ['hu']
}
constructed_url = endpoint + path

headers = {
    'Ocp-Apim-Subscription-Key': subscription_key,
    'Ocp-Apim-Subscription-Region': location,
    'Content-type': 'application/json',
    'X-ClientTraceId': str(uuid.uuid4())
}

# You can pass more than one object in body.
body = [{
    'text': 'The Severn Railway Bridge ( historically called the Severn Bridge ) was a bridge carrying the railway across the River Severn between Sharpness and Lydney,Gloucestershire.'
    #'A famous bridge in New Taipei City is the Taipei Bridge, connecting New Taipei City with Taipei over the Tamsui River .'
}]

request = requests.post(constructed_url, params=params, headers=headers, json=body)
response = request.json()

magyarmondat = response[0]["translations"][0]["text"]
magyarprojekcio = response[0]["translations"][0]["alignment"]["proj"]
print(magyarmondat)
print(magyarprojekcio)
print(json.dumps(response, sort_keys=True, ensure_ascii=False, indent=4, separators=(',', ': ')))