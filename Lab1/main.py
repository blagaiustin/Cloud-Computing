import requests

url = "https://currency-exchange.p.rapidapi.com/exchange"

querystring = {"from":"EUR","to":"USD","q":"1.0"}

headers = {
    'x-rapidapi-host': "currency-exchange.p.rapidapi.com",
    'x-rapidapi-key': "a306a1c3d9mshddcc53145160dfep1ee906jsn8cc5988c5e86"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

output = open("rate.txt", "w")

output.write(str(int(float(response.text))))