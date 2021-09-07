import requests
import json
import re
import threading
import time

API_KEY = "toFoJCyvQXL1"
PROJECT_TOKEN = "tX7kX2mrfT6u"
RUN_TOKEN = "tukaEYQ-zzUq"


def r(string):
    replace = string.replace(',', '')
    return replace


class Data:

    def __init__(self, api_key, project_token):
        self.api_key = api_key
        self.project_token = project_token
        self.params = {
            "api_key": self.api_key
        }
        self.data = self.get_data()

    def get_data(self):
        response = requests.get(f'https://www.parsehub.com/api/v2/projects/{self.project_token}/last_ready_run/data',
                                params=self.params)
        data = json.loads(response.text)
        return data

    def get_total_cases(self):
        data = self.data['total']

        for content in data:
            if content['name'] == "Coronavirus Cases:":
                print(content['value'])
                return content['value']

    def get_total_deaths(self):
        data = self.data['total']

        for content in data:
            if content['name'] == "Deaths:":
                print(content['value'])
                return content['value']

        return "0"

    def get_country_data(self, country, string='total_cases'):
        data = self.data["country"]

        for content in data:
            if content['name'].lower() == country.lower():
                print(content[string])
                return content

        return "0"

    def get_list_of_countries(self):
        countries = []
        for country in self.data['country']:
            countries.append(country['name'].lower())

        return countries

    def get_total_recovered(self):
        data = self.data['total']

        for content in data:
            if content['name'] == "Recovered:":
                print(content['value'])
                return content['value']

        return "0"

    def get_total_active(self):
        active = int(r(self.get_total_cases())) - int(r(self.get_total_recovered())) - int(r(self.get_total_deaths()))
        print(active)
        return active

    def update_data(self):
        response = requests.post(f'https://www.parsehub.com/api/v2/projects/{self.project_token}/run',
                                 params=self.params)

        def poll():
            time.sleep(0.1)
            old_data = self.data
            while True:
                new_data = self.get_data()
                if new_data != old_data:
                    self.data = new_data
                    print("Data updated")
                    break
                time.sleep(5)

        t = threading.Thread(target=poll)
        t.start()


data = Data(API_KEY, PROJECT_TOKEN)

country_list = data.get_list_of_countries()

