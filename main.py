import requests

# url = "http://54.180.108.110:5000/findway"
url = "http://127.0.0.1:5000/json/"
data = {
    "building_name": "CAU310",
    "startFloor": 2,
    "startId": 5,
    "endFloor": 5,
    "endId": 40,
    "elev": 0,
}
filename = "CAU310_01"

response = requests.get(url + filename)
print(response.json())
