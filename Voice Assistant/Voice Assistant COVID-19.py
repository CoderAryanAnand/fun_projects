import requests
import json
import pyttsx3
import speech_recognition as sr
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

    def get_country_data(self, country, string):
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


def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def get_audio():
    rec = sr.Recognizer()
    with sr.Microphone() as source:
        audio = rec.listen(source)
        said = ""

        try:
            said = rec.recognize_google(audio)
        except Exception as e:
            print("Exception:", str(e))

    return said.lower()


def main():
    print("Started Program")
    data = Data(API_KEY, PROJECT_TOKEN)
    END_PHRASE = "stop"
    country_list = data.get_list_of_countries()

    TOTAL_PATTERNS = {
        re.compile("[\w\s]+ total [\w\s]+ cases"): data.get_total_cases,
        re.compile("[\w\s]+ total cases"): data.get_total_cases,
        re.compile("[\w\s]+ worldwide [\w\s]+ cases"): data.get_total_cases,
        re.compile("[\w\s]+ worldwide cases"): data.get_total_cases,
        re.compile("[\w\s]+ total [\w\s]+ cases worldwide"): data.get_total_cases,
        re.compile("[\w\s]+ cases worldwide"): data.get_total_cases,  #
        re.compile("[\w\s]+ total [\w\s]+ deaths"): data.get_total_deaths,
        re.compile("[\w\s]+ total deaths"): data.get_total_deaths,
        re.compile("[\w\s]+ worldwide [\w\s]+ deaths"): data.get_total_deaths,
        re.compile("[\w\s]+ worldwide deaths"): data.get_total_deaths,
        re.compile("[\w\s]+ total [\w\s]+ deaths worldwide"): data.get_total_deaths,
        re.compile("[\w\s]+ deaths worldwide"): data.get_total_deaths,
        re.compile("[\w\s]+ total [\w\s]+ recovered"): data.get_total_recovered,
        re.compile("[\w\s]+ total recovered"): data.get_total_recovered,
        re.compile("[\w\s]+ worldwide [\w\s]+ recovered"): data.get_total_recovered,
        re.compile("[\w\s]+ worldwide recovered"): data.get_total_recovered,
        re.compile("[\w\s]+ total [\w\s]+ recovered worldwide"): data.get_total_recovered,
        re.compile("[\w\s]+ recovered worldwide"): data.get_total_recovered,
        re.compile("[\w\s]+ total [\w\s]+ active"): data.get_total_active,
        re.compile("[\w\s]+ total active"): data.get_total_active,
        re.compile("[\w\s]+ worldwide [\w\s]+ active"): data.get_total_active,
        re.compile("[\w\s]+ worldwide active"): data.get_total_active,
        re.compile("[\w\s]+ total [\w\s]+ active worldwide"): data.get_total_active,
        re.compile("[\w\s]+ active worldwide"): data.get_total_active,
    }

    COUNTRY_PATTERNS = {
        re.compile("[\w\s]+ cases [\w\s]+"): lambda country: data.get_country_data(country, 'total_cases')['total_cases'],
        re.compile("[\w\s]+ deaths [\w\s]+"): lambda country: data.get_country_data(country, 'total_deaths')['total_deaths'],
        re.compile("[\w\s]+ recovered [\w\s]+"): lambda country: data.get_country_data(country, 'total_recovered')['total_recovered'],
        re.compile("[\w\s]+ active [\w\s]+"): lambda country: data.get_country_data(country, 'total_active')['total_active']
    }

    UPDATE_COMMAND = "update"

    while True:
        print("Listening...")
        text = get_audio()
        print(text)
        result = None

        for pattern, func in COUNTRY_PATTERNS.items():
            if pattern.match(text):
                words = set(text.split(" "))
                for country in country_list:
                    if country in words:
                        result = func(country)
                        break

        for pattern, func in TOTAL_PATTERNS.items():
            if pattern.match(text):
                result = func()
                break

        if text == UPDATE_COMMAND:
            result = "Data is being updated. This may take a moment!"
            data.update_data()

        if result:
            speak(result)

        if text.find(END_PHRASE) != -1:  # stop loop
            print("Exit")
            break


main()