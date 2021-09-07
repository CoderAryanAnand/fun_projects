import datetime
import pickle
import smtplib
import subprocess
from GoogleNews import GoogleNews
import pywhatkit as kit
import tkinter as tk
from bs4 import BeautifulSoup
from getpass import getpass

import pytz
import time as tm
import speech_recognition as sr  # importing speech recognition package from google api
import requests
import playsound  # to play saved mp3 file
import wikipedia
from gtts import gTTS  # google text to speech
import os  # to save/open files
import wolframalpha  # to calculate strings into formula, its a website which provides api, 100 times per day
from selenium import webdriver  # to control browser operations
from selenium.webdriver.common.keys import Keys
from io import BytesIO
from io import StringIO
import webbrowser
# from webdriver_manager.chrome import ChromeDriverManager
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pyautogui
import psutil
import pyjokes
import numpy as np
# import cv2
# import face_recognition

# from face_rec_test import *

# name = ''
#
# video_capture = cv2.VideoCapture(0)
#
# aryan_image = face_recognition.load_image_file('known/aryan.jpg')
#
# aryan_face_encoding = face_recognition.face_encodings(aryan_image)[0]
#
# known_face_encodings = [aryan_face_encoding]
# known_face_names = ['Aryan']

driver = webdriver.Chrome(
    executable_path=r"C:\Users\Aryan\.wdm\drivers\chromedriver\chromedriver.exe")

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
MONTHS = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november",
          "december"]
DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
DAY_EXT = ["rd", "th", "st", "nd"]
WAKE = "jarvis"
num = 1
webbrowser.Mozilla()
date = datetime.datetime.today().date().strftime('%d/%m/%Y')
googlenews = GoogleNews(lang='en', period='d', start=date, end=date)
root = tk.Tk()

pyautogui.hotkey('winleft', 'down')


def speak(output):
    global num
    num += 1
    print("JARVIS: ", output)
    toSpeak = gTTS(text=output, lang='en-US', slow=False)
    file = str(num) + ".mp3"
    toSpeak.save(file)
    playsound.playsound(file, True)
    os.remove(file)


def get_audio():
    r = sr.Recognizer()
    audio = ''
    with sr.Microphone() as source:
        print("Speak...")
        audio = r.listen(source, phrase_time_limit=20)
    print("Stop.")
    try:
        text = r.recognize_google(audio, language='en-in')
        print("You: ", text)
        return text.lower()
    except:
        #  speak("Could not understand your audio, PLease try again!")
        return '0'


def get_alarm_audio():
    r = sr.Recognizer()
    audio = ''
    with sr.Microphone() as source:
        print("Speak...")
        audio = r.listen(source, phrase_time_limit=1)
    print("Stop.")
    try:
        text = r.recognize_google(audio, language='en-in')
        print("You: ", text)
        return text.lower()
    except:
        #  speak("Could not understand your audio, PLease try again!")
        return '0'


def send_mail():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    speak('What is the content?')

    body = input('What is the content?')
    server.login('email', 'wbjcfgttltoghllk')
    subject = 'From JARVIS'

    speak('To whom are you sending this? Please write below.')
    receiver = input('To whom are you sending this?')

    msg = f"Subject: {subject}\n\n{body}"

    server.sendmail(
        'JARVIS',
        receiver,
        msg
    )


def search_web(input):
    """    driver = webdriver.Edge()
    driver.implicitly_wait(1)"""
    global indx
    if 'youtube' in input.lower():
        speak("Opening in youtube")
        indx = input.lower().split().index('youtube')
        query = input.split()[indx + 1:]
        if query[0] == 'for':
            del query[0]
        else:
            pass
        driver.get(url="http://www.youtube.com/results?search_query=" + ''.join(query))
        """ speak('What do you want to search?')
        search_que = get_audio()
        search_box = driver.find_element_by_xpath(
            '//*[@id="search"]')
        search_box.send_keys(search_que)
        search_button = driver.find_element_by_xpath(
            '//*[@id="search-icon-legacy"]')
        search_button.click()"""

        return

    elif 'wikipedia' in input.lower() or 'who is' in input.lower() or 'what is' in input.lower():
        speak("searching in wikipedia")
        query = input.replace("wikipedia", "")
        query = input.replace("who is", "")
        query = input.replace("what is", "")
        results = wikipedia.summary(query, sentences=2)
        speak("According to wikipedia")
        speak(results)
        return
    else:
        if 'google' or 'internet' or 'web' in input:
            try:
                indx = input.lower().split().index('google for')
                query = input.split()[indx + 1:]
                if query[0] == 'for':
                    del query[0]
                else:
                    pass
                webbrowser.open(url="https://www.google.com/search?q=" + ''.join(query))
            except ValueError:
                webbrowser.open(url="https://www.google.com/search?q=" + ''.join(input.split()))

        elif 'search' in input:
            try:
                indx = input.lower().split().index('google')
            except ValueError:
                webbrowser.open(url="https://www.google.com/search?q=" + ''.join(input.split()))
            query = input.split()[indx + 1:]
            if query[0] == 'for':
                del query[0]
            else:
                pass
            webbrowser.open(url="https://www.google.com/search?q=" + ''.join(query))
        else:
            webbrowser.open(url="https://www.google.com/search?q=" + ''.join(input.split()))
        return


def note(txr):
    da = datetime.datetime.now()
    file_name = 'D:\\Voice Assistant\\notes\\' + str(da).replace(":", "-") + "-note.txt"
    with open(file_name, "w") as f:
        f.write(txr)

    subprocess.Popen(["notepad.exe", file_name])


def authenticate_google():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    return service


def get_events(day, service):
    # Call the Calendar API
    date = datetime.datetime.combine(day, datetime.datetime.min.time())
    end_date = datetime.datetime.combine(day, datetime.datetime.max.time())
    utc = pytz.UTC
    date = date.astimezone(utc)
    end_date = end_date.astimezone(utc)

    events_result = service.events().list(calendarId='primary', timeMin=date.isoformat(), timeMax=end_date.isoformat(),
                                          singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        speak('No upcoming events found.')
    else:
        speak(f"You have {len(events)} events on this day.")

        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])
            start_time = str(start.split("T")[1].split("-")[0])
            if int(start_time.split(":")[0]) < 12:
                start_time = start_time + "am"
            else:
                start_time = str(int(start_time.split(":")[0]) - 12) + start_time.split(":")[1]
                start_time = start_time + "pm"

            speak(event["summary"] + " at " + start_time)


def get_date(txr):
    txr = txr.lower()
    today = datetime.date.today()

    if txr.count("today") > 0:
        return today

    day = -1
    day_of_week = -1
    month = -1
    year = today.year

    for word in txr.split():
        if word in MONTHS:
            month = MONTHS.index(word) + 1
        elif word in DAYS:
            day_of_week = DAYS.index(word)
        elif word.isdigit():
            day = int(word)
        else:
            for ext in DAY_EXT:
                found = word.find(ext)
                if found > 0:
                    try:
                        day = int(word[:found])
                    except Exception as e:
                        print(e)
                        pass

    # THE NEW PART STARTS HERE
    if month < today.month and month != -1:  # if the month mentioned is before the current month set the year to the
        # next
        year = year + 1

    # This is slightly different from the video but the correct version
    if month == -1 and day != -1:  # if we didn't find a month, but we have a day
        if day < today.day:
            month = today.month + 1
        else:
            month = today.month

    # if we only found a dta of the week
    if month == -1 and day == -1 and day_of_week != -1:
        current_day_of_week = today.weekday()
        dif = day_of_week - current_day_of_week

        if dif < 0:
            dif += 7
            if txr.count("next") >= 1:
                dif += 7

        return today + datetime.timedelta(dif)

    if day != -1:  # FIXED FROM VIDEO
        return datetime.date(month=month, day=day, year=year)


def open_application(inp):
    if "chrome" in inp:
        speak("Google Chrome")
        os.startfile(r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe')
        return
    elif "firefox" in inp or "mozilla" in inp:
        speak("Opening Mozilla Firefox")
        os.startfile(r'C:\Program Files\Mozilla Firefox\\firefox.exe')
        return
    elif "word" in inp:
        speak("Opening Microsoft Word")
        os.startfile(r'C:\ProgramData\Microsoft\Windows\Start Menu\Programs\\Word')
        return
    elif "excel" in inp:
        speak("Opening Microsoft Excel")
        os.startfile(r'C:\ProgramData\Microsoft\Windows\Start Menu\Programs\\Excel')
        return
    else:
        speak("Application not available")
        return


def open_link(url):
    driver.get(url)


"""def get_news(news):
    googlenews.clear()
    googlenews.search(str(news))
    googlenews.getpage(1)
    result = googlenews.result()

    art = dict()
    root.geometry('400x400')

    for i in range(len(result)):
        title = result[i]['title']
        desc = result[i]['desc']
        url = result[i]['link']
        source = result[i]['media']
        a_date = result[i]['date']
        art[title] = title, desc, source, a_date, url
        list_temp = [title, desc, a_date, source]
        tk.Button(root, text='\n'.join(list_temp), command=lambda: open_link(url=url)).pack()
    tk.Scrollbar(root).pack(side='right', fill='y')
    root.mainloop()

    root.title('News')"""


def time():
    ct = [int(datetime.datetime.now().strftime('%I')), int(datetime.datetime.now().strftime('%M')),
          datetime.datetime.now().strftime('%p')]
    speak('The current time is: ')
    speak(' '.join(map(str, ct)))


def date():
    dt = [int(datetime.datetime.now().day), int(datetime.datetime.now().month), int(datetime.datetime.now().year)]
    speak('The current date is: ')
    speak('/'.join(map(str, dt)))


def play_song(song_name):
    print('d')
    song_name = song_name.lower()
    print('q')
    song = song_name.replace('play', '')
    print(song)
    kit.playonyt(song)
    print('r')


def satw(path, number):
    tm.sleep(6)
    webbrowser.open(f'https://web.whatsapp.com/send?phone={number}')
    pyautogui.hotkey('winleft', 'up')
    pyautogui.click(2839, 173)
    pyautogui.click(2858, 281)
    pyautogui.typewrite(['*', '.', '*', 'enter'])
    pyautogui.typewrite(path)
    pyautogui.typewrite(['enter'])
    tm.sleep(2)
    pyautogui.click(2836, 1869)


def wish_me(name):
    hour = datetime.datetime.now().hour
    if 6 <= hour < 12:
        speak(f'Good Morning! Welcome back, {name}!')
    elif 12 <= hour < 18:
        speak(f'Good Afternoon! Welcome back, {name}!')
    elif 18 <= hour < 22:
        speak(f'Good Evening! Welcome Back, {name}!')
    else:
        speak('Good Night! Welcome Back!')
    speak('I am Jarvis your Personal Assistant.')


def screenshot():
    da = datetime.datetime.now()
    file_name = 'D:\\Voice Assistant\\photos\\' + str(da).replace(":", "-") + "-screenshot.png"
    img = pyautogui.screenshot()
    img.save(file_name)


def cpu():
    usage = str(psutil.cpu_percent())
    speak('CPU is at ' + usage + ' percent.')
    battery = str(psutil.sensors_battery().percent)
    if psutil.sensors_battery().power_plugged:
        speak('Battery is at ' + battery + ' percent and is plugged in.')
    else:
        speak('Battery is at ' + battery + ' percent and is not plugged in.')


def jokes():
    speak(pyjokes.get_joke())


def process_text(inp):
    service = authenticate_google()
    inp = inp.lower()
    try:
        if "who are you" in inp or "define yourself" in inp:
            te = '''Hello, I am Jarvis. Your personal Assistant.
            I am here to make your life easier. 
            You can command me to perform various tasks such as calculating sums or opening applications etcetra'''
            speak(te)
            return
        elif "who made you" in inp or "created you" in inp:
            te = "I have been created by Aryan."
            speak(te)
            return
        elif "crazy" in inp:
            te = """Well, there are many mental asylums in the world."""
            speak(te)
            return
        elif 'news' in inp:
            speak("I didn't quite understand what I should search for. Could you say what exactly I should search for?")
            nsew = get_audio()
            driver.get('https://news.google.com/topstories?hl=en-US&gl=US&ceid=US:en+')
            search = driver.find_element_by_xpath('//*[@id="gb"]/div[2]/div[2]/div/form/div['
                                                  '1]/div/div/div/div/div[1]/input[2]')
            search.send_keys(nsew)
            search.send_keys(Keys.ENTER)
        elif "calculate" in inp.lower():
            app_id = "WE385L-PWLLYRUVQQ"
            client = wolframalpha.Client(app_id)

            inn = inp.lower().split().index('calculate')
            query = inp.split()[inn + 1:]
            res = client.query(' '.join(query))
            answer = next(res.results).text
            speak("The answer is " + answer)
            return
        elif 'cpu' in inp:
            cpu()
        if 'joke' in inp and 'what' not in inp:
            jokes()
        elif 'open' in inp:
            pyautogui.press('winleft')
            pyautogui.typewrite(inp.lower())
            pyautogui.typewrite(['enter'])
            return
        elif 'send' in inp and 'mail' in inp:
            send_mail()
        elif 'send' in inp and 'message' in inp:
            rec = inp.replace('send', '')
            rec = rec.replace('whatsapp', '')
            rec = rec.replace('to', '', 1)
            rec = rec.replace('with', '')
            rec = rec.replace('in', '')
            rec = rec.replace('saying', '')
            rec = rec.replace('message', '')
            rec = rec.replace('through', '')
            rec = rec.replace('a', '', 1)
            rec = rec.replace(' ', '')

            speak('what is the content?')
            message = get_audio()
            webbrowser.open('https://web.whatsapp.com/send?phone=' + peo[rec] + '&text=' + message)
            tm.sleep(30)
            pyautogui.typewrite(['enter'])
        elif 'attachment' and 'message' in inp:
            speak('Please enter the path')
            a = input()
            rec = inp.replace('send', '')
            rec = rec.replace('whatsapp', '')
            rec = rec.replace('to', '', 1)
            rec = rec.replace('with', '')
            rec = rec.replace('in', '')
            rec = rec.replace('saying', '')
            rec = rec.replace('message', '')
            rec = rec.replace('through', '')
            rec = rec.replace('a', '', 1)
            rec = rec.replace('an', '', 1)
            rec = rec.replace('attachment', '')
            rec = rec.replace('ttchment', '')
            rec = rec.replace(' ', '')
            satw(a, peo[rec])
        elif 'play' in inp and 'game' not in inp and 'games' not in inp:
            play_song(inp)
        elif 'weather' in inp:
            info = requests.get('https://ipinfo.io')
            data = info.json()
            city = data['city']
            region = data['region']
            country = data['country']
            # lat, long = data['loc'].split(',')[0], data['loc'].split(',')[1]
            # api_key = 'b6a9b24c776284b615e6e71f2a303997'
            # complete_url = f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon=-{long}&exclude=minutely&appid={api_key}'
            # response = '0'
            # while str(response) != '<Response [200]>':
            #     response = requests.get(complete_url)
            #     x = response.json()
            # speak(
            #     'The current weather is {} degrees, but it feels like {} degrees.'.format(round(x['main']['temp'], 0),
            #                                                                               round(x['main']['feels_like'], 0)
            #                                                                               )
            # )
            # if x['weather'][0]['main'] == 'Thunderstorm':
            #     speak('There is going to be a Thunderstorm! Be Careful!')
            # elif x['weather'][0]['main'] == 'Drizzle':
            #     speak("It's going to drizzle!")
            # elif x['weather'][0]['main'] == 'Rain':
            #     if x['weather'][0]['id'] == 500:
            #         speak("It's going to rain lightly!")
            #     elif x['weather'][0]['id'] == 501 or 520 or 521:
            #         speak('The rain is going to be moderate.')
            #     elif x['weather'][0]['id'] == 502 or 503 or 504 or 511 or 531 or 522:
            #         speak("It's going to rain heavily!")
            # elif x['weather'][0]['main'] == 'Snow':
            #     if x['weather'][0]['id'] == 620 or 612 or 600 or 615:
            #         speak("It's going to snow lightly!")
            #     elif x['weather'][0]['id'] == 601 or 621 or 616 or 613:
            #         speak("It's going to snow!")
            #     else:
            #         speak("It's going to snow heavily!")
            # elif x['weather'][0]['main'] == 'Clear':
            #     speak("It's clear!")
            # elif x['weather'][0]['main'] == 'Clouds':
            #     speak('It is cloudy!')
            # else:
            #     speak(f"There is a {x['weather'][0]['description']}! Be careful!")
            app_id = "WE385L-PWLLYRUVQQ"
            client = wolframalpha.Client(app_id)
            result = client.query('weather forecast for' + city + ', ' + country)
            weather = next(result.results).text
            w = weather.split('\n')
            speak('The weather is ' + w[0] + ' and is ' + w[1])
        elif "make a note" in inp or "write this down" in inp or "remember this" in inp:
            speak('What do you want to make a note of?')
            note_text = get_audio()
            note(note_text)
            speak('Saved in notes folder!')
        elif "what do i have" in inp or "do i have plans" in inp or "am i busy" in inp:
            da = get_date(text)
            if da:
                get_events(da, service)
            else:
                speak("I don't understand")
        elif 'search' in inp or 'play' in inp or 'who is' in inp or 'what is' in inp or 'what' in inp and \
                'news' not in inp:
            search_web(inp.lower())
            return
        elif 'the time' in inp:
            time()
        elif 'logout' in inp:
            os.system('shutdown -l')
        elif 'shutdown' in inp:
            os.system('shutdown /s /t 1')
        elif 'restart' in inp:
            os.system('shutdown /r /t 1')
        elif 'screenshot' in inp:
            screenshot()
            speak('Saved in photos folder!')
        else:
            speak("I can search the web for you, Do you want to continue?")
            ans = get_audio()
            if 'yes' in str(ans) or 'yeah' in str(ans):
                search_web(inp)
            else:
                return
    except Exception as e:
        print(e)
        # speak("I don't understand, I'm searching the web'")
        # search_web(input)


password = {'margi123': 'Aryan'}
pa = ''
if __name__ == "__main__":
    # while pa not in password:
    #     pa = getpass(prompt='Password: ')
    # name = password[pa]
    info = requests.get('https://ipinfo.io')
    data = info.json()
    city = data['city']
    country = data['country']
    app_id = "WE385L-PWLLYRUVQQ"
    client = wolframalpha.Client(app_id)
    result = client.query('weather forecast for' + city + ', ' + country)
    weather = next(result.results).text
    w = weather.split('\n')
    text = '10000'
    while text.count(WAKE) < 1:
        speak('Get up!!')
        text = get_alarm_audio()
    wish_me('Aryan')
    speak('The weather is ' + w[0] + ' and is ' + w[1])
    while True:
        text = get_audio()
        try:
            if text.count(WAKE) > 0:
                speak("What can i do for you?")
                text = get_audio()
                if text == 0:
                    continue
                # speak(text)
                if "exit" in str(text) or "bye" in str(text) or "sleep" in str(text) or "stop" in str(
                        text) or 'offline' in \
                        str(text):
                    speak("Ok bye, " + 'Aryan' + '.')
                    quit()
                    exit()
                    break
                process_text(text)
            else:
                pass
        except AttributeError:
            pass
