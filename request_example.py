import requests

headers = {
    'accept': 'application/json',
}

params = {
    'token': '12345',
    'max_request_per_minutes': '1',
}

response = requests.get('http://127.0.0.1:8000/check', headers=headers, params=params)
print(response.json())
# {'response': True}
# {'response': False}
