import json
import requests


url = "https://numbers-spell.p.rapidapi.com/numbers"

rate_file = open("rate.txt", "r")
rate = rate_file.read()

querystring1 = '{\"text\":\"' + rate + '\"}'

covid_file = open("covid.json", "r")
covid_data = json.loads(covid_file.read())
death_count = covid_data['New Deaths_text']

querystring2 = '{\"text\":\"' + death_count + '\"}'

headers = {
    'x-funtranslations-api-secret': "23486",
    'x-rapidapi-host': "numbers-spell.p.rapidapi.com",
    'x-rapidapi-key': "a306a1c3d9mshddcc53145160dfep1ee906jsn8cc5988c5e86"
    }

response1 = requests.request("GET", url, headers=headers, params=querystring1)
print(response1.text)

response2 = requests.request("GET", url, headers=headers, params=querystring2)
print(response2.text)