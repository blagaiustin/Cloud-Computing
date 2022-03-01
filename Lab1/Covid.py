import requests

url = "https://covid-19-tracking.p.rapidapi.com/v1/usa"

headers = {
    'x-rapidapi-host': "covid-19-tracking.p.rapidapi.com",
    'x-rapidapi-key': "a306a1c3d9mshddcc53145160dfep1ee906jsn8cc5988c5e86"
    }

response = requests.request("GET", url, headers=headers)

output = open("covid.json", "w")

output.write(response.text)