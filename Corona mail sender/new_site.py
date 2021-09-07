import requests
import json

url = "https://covid-193.p.rapidapi.com/statistics"

querystring = {"country":"switzerland"}

headers = {
    'x-rapidapi-host': "covid-193.p.rapidapi.com",
    'x-rapidapi-key': "77ac734d58msh1a79ee0f681dfb8p190ccejsnd5efcac79b67"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

r = json.loads(response.text)
re = r['response'][0]
