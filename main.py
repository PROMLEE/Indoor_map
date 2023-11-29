import requests

url = "http://54.180.106.175:5000/way"
# url = "http://127.0.0.1:5000/way"
data = {
    "building_name": "CAU310",
    "startFloor": 2,
    "startId": 5,
    "endFloor": 5,
    "endId": 40,
    "elev": 1,
}

response = requests.post(url, json=data)
if response.status_code == 200:
    print("Response from server")
else:
    print("Error in API call")
