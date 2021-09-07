from time import sleep
import smtplib
import os
import pyautogui
import webbrowser
import requests
import json

url = "https://covid-193.p.rapidapi.com/statistics"

querystring = {"country": "switzerland"}

headers = {
    'x-rapidapi-host': "covid-193.p.rapidapi.com",
    'x-rapidapi-key': "77ac734d58msh1a79ee0f681dfb8p190ccejsnd5efcac79b67"
}

response = requests.request("GET", url, headers=headers, params=querystring)

r = json.loads(response.text)
re = r['response'][0]


def get_data():
    send_mail('Switzerland', re['cases']['total'], re['cases']['new'], re['deaths']['total'], re['deaths']['new'],
              re['cases']['active'], re['cases']['recovered'], re['cases']['critical'])


def send_mail(country_element, total_cases, new_cases, total_deaths, new_deaths, active_cases, total_recovered,
              serious_critical):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login('email', 'wbjcfgttltoghllk')

    subject = 'Coronavirus stats in your country today!'

    body = 'Today in ' + str(country_element) + ',' + '\
        \nThere is new data on coronavirus:\
        \nTotal cases: ' + str(total_cases) + '\
        \nNew cases: ' + str(new_cases) + '\
        \nTotal deaths: ' + str(total_deaths) + '\
        \nNew Deaths: ' + str(new_deaths) + '\
        \nActive cases: ' + str(active_cases) + '\
        \nTotal recovered: ' + str(total_recovered) + '\
        \nSerious, critical cases: ' + str(serious_critical) + '\
        \nCheck the link: https://www.worldometers.info/coronavirus/'

    msg = f"Subject: {subject}\n\n{body}"

    server.sendmail(
        'Coronavirus',
        'email',
        msg
    )
    server.sendmail(
        'Coronavirus',
        'email',
        msg
    )
    server.sendmail(
        'Coronavirus',
        'email',
        msg
    )
    # if new_deaths == '':
    #     new_deaths = '0'
    # if new_cases == '':
    #     new_cases = '0'
    # body = f'Today in {country_element} there is new data on COVID-19! Total cases: *{total_cases}*; New cases:'\
    #        f' *{new_cases.replace("+", "")}*; Total deaths: *{total_deaths}*; New deaths:'\
    #        f' *{new_deaths.replace("+", "")}*;'\
    #        f' Active cases: *{active_cases}*; Total recovered: *{total_recovered}*;'\
    #        f' Serious, critical cases: *{serious_critical}*; *Check the link:* '\
    #        f'https://www.worldometers.info/coronavirus/country/switzerland '
    # webbrowser.open('https://web.whatsapp.com/send?phone=' + '+num' + '&text=' + body)
    # sleep(30)
    # pyautogui.typewrite(['enter'])
    # webbrowser.open('https://web.whatsapp.com/send?phone=' + '+num' + '&text=' + body)
    # sleep(30)
    # pyautogui.typewrite(['enter'])
    # webbrowser.open('https://web.whatsapp.com/send?phone=' + '+num' + '&text=' + body)
    # sleep(30)
    # pyautogui.typewrite(['enter'])

    server.quit()
    # sleep(10)
    # os.system('shutdown /s /t 1')


get_data()
