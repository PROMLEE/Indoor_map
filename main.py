import requests

url = 'http://54.180.106.175/run-way'
data = {
    'value1': '값1',
    'value2': '값2',
    'value3': '값3',
    'value4': '값4'
}

response = requests.post(url, json=data)
if response.status_code == 200:
    print("Response from server:", response.json())
else:
    print("Error in API call")
