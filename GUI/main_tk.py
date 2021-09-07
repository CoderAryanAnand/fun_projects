from tkinter import *
import os
import subprocess
import webbrowser
import time

import psutil
import requests
import wolframalpha
from PIL import ImageTk, Image

root = Tk()
root.title("GUI")

# Create a photoimage object of the image in the path
image1 = Image.open("images/bg1.png")
test = ImageTk.PhotoImage(image1)

label1 = Label(root, image=test)
label1.image = test

# Position image
label1.place(x=0, y=0)

# root.configure(bg="black")


root.geometry("1819x1211")
root.resizable(0, 0)
root.wm_attributes('-transparentcolor', 'grey')


# Start time label
def time_label():
    string = time.strftime('%H:%M:%S')
    timeLabel.config(text=string)
    timeLabel.after(1000, time_label)


timeLabel = Label(root, font=("ds-digital", 80), background="grey", foreground="cyan")
timeLabel.place(x=745, y=50)
time_label()


# End time label

# # Start cpu memory label
# def cpu_usage():
#     cpu = psutil.cpu_percent(1)
#     together = "CPU usage: " + str(cpu) + "%"
#     if cpu > 50:
#         cpuLabel.config(text=together, foreground="red")
#     else:
#         cpuLabel.config(text=together, foreground="cyan")
#     cpuLabel.after(100, cpu_usage)
#
#
# cpuLabel = Label(root, font=("ds-digital", 30), background="black", foreground="cyan")
# cpuLabel.place(x=100, y=150)
# cpu_usage()
#
#
# def memory_usage():
#     memory = psutil.virtual_memory().percent
#     together = f"Memory usage: {memory}%"
#     memLabel.config(text=together)
#     memLabel.after(1000, memory_usage)
#
#
# memLabel = Label(root, font=("ds-digital", 30), background="black", foreground="cyan")
# memLabel.place(x=100, y=200)
# memory_usage()
#
#
# # End cpu memory label
# # Start favourite Apps/Links
# def open_app_link(name):
#     if name == 'wa':
#         webbrowser.open("https://web.whatsapp.com/")
#     elif name == 'yt':
#         webbrowser.open("https://www.youtube.com/")
#     elif name == 'mc':
#         subprocess.run(r"C:\Program Files (x86)\Minecraft Launcher\MinecraftLauncher.exe")
#     elif name == 'gh':
#         webbrowser.open("https://www.github.com/")
#     elif name == 'gm':
#         webbrowser.open("https://mail.google.com/mail/u/0/#inbox")
#     elif name == 'cmd':
#         subprocess.run("wt.exe")
#
#
# ytPhoto = PhotoImage(file="images/Youtube.png").subsample(13, 13)
# waPhoto = PhotoImage(file="images/Whatsapp.png").subsample(18, 18)
# mcPhoto = PhotoImage(file="images/Minecraft block.png").subsample(14, 14)
# ghPhoto = PhotoImage(file="images/Github.png").subsample(46, 46)
# gmPhoto = PhotoImage(file="images/Gmail.png").subsample(9, 9)
# cmdPhoto = PhotoImage(file="images/cmd.png").subsample(3, 3).zoom(2, 2)
# ytButton = Button(root,
#                   image=ytPhoto, command=lambda: open_app_link('yt'),
#                   background="black", borderwidth=0, cursor="hand2")
# waButton = Button(root,
#                   image=waPhoto, command=lambda: open_app_link('wa'),
#                   background="black", borderwidth=0, cursor="hand2")
# mcButton = Button(root,
#                   image=mcPhoto, command=lambda: open_app_link('mc'),
#                   background="black", borderwidth=0, cursor="hand2")
# ghButton = Button(root,
#                   image=ghPhoto, command=lambda: open_app_link('gh'),
#                   background="black", borderwidth=0, cursor="hand2")
# gmButton = Button(root,
#                   image=gmPhoto, command=lambda: open_app_link('gm'),
#                   background="black", borderwidth=0, cursor="hand2")
# cmdButton = Button(root,
#                    image=cmdPhoto, command=lambda: open_app_link('cmd'),
#                    background="black", borderwidth=0, cursor="hand2")
#
# ytButton.place(x=1000, y=150)
# waButton.place(x=1087, y=150)
# mcButton.place(x=1149, y=150)
# ghButton.place(x=1210, y=150)
# gmButton.place(x=1275, y=150)
# cmdButton.place(x=1355, y=150)
#
#
# def enterYt(e=True):
#     ytButton.configure(background='light grey')
#     if e:
#         pass
#     else:
#         pass
#
#
# def leaveYt(e=True):
#     ytButton.configure(background='black')
#     if e:
#         pass
#     else:
#         pass
#
#
# ytButton.bind('<Enter>', enterYt)
# ytButton.bind('<Leave>', leaveYt)
#
#
# def enterWa(e=True):
#     waButton.configure(background='light grey')
#     if e:
#         pass
#     else:
#         pass
#
#
# def leaveWa(e=True):
#     waButton.configure(background='black')
#     if e:
#         pass
#     else:
#         pass
#
#
# waButton.bind('<Enter>', enterWa)
# waButton.bind('<Leave>', leaveWa)
#
#
# def enterMc(e=True):
#     mcButton.configure(background='light grey')
#     if e:
#         pass
#     else:
#         pass
#
#
# def leaveMc(e=True):
#     mcButton.configure(background='black')
#     if e:
#         pass
#     else:
#         pass
#
#
# mcButton.bind('<Enter>', enterMc)
# mcButton.bind('<Leave>', leaveMc)
#
#
# def enterGh(e=True):
#     ghButton.configure(background='light grey')
#     if e:
#         pass
#     else:
#         pass
#
#
# def leaveGh(e=True):
#     ghButton.configure(background='black')
#     if e:
#         pass
#     else:
#         pass
#
#
# ghButton.bind('<Enter>', enterGh)
# ghButton.bind('<Leave>', leaveGh)
#
#
# def enterGm(e=True):
#     gmButton.configure(background='light grey')
#     if e:
#         pass
#     else:
#         pass
#
#
# def leaveGm(e=True):
#     gmButton.configure(background='black')
#     if e:
#         pass
#     else:
#         pass
#
#
# gmButton.bind('<Enter>', enterGm)
# gmButton.bind('<Leave>', leaveGm)
#
#
# def enterCmd(e=True):
#     cmdButton.configure(background='light grey')
#     if e:
#         pass
#     else:
#         pass
#
#
# def leaveCmd(e=True):
#     cmdButton.configure(background='black')
#     if e:
#         pass
#     else:
#         pass
#
#
# cmdButton.bind('<Enter>', enterCmd)
# cmdButton.bind('<Leave>', leaveCmd)
#
#
# # End favourite Apps/Links
# # Start weather
# def get_current_weather():
#     # Based on ip address
#     info = requests.get('https://ipinfo.io')
#     data = info.json()
#     city = data['city']
#     # region = data['region']
#     country = data['country']
#     app_id = "WE385L-PWLLYRUVQQ"
#     client = wolframalpha.Client(app_id)
#     result = client.query('weather forecast ' + city + ', ' + country)
#     weather = next(result.results).text
#     w = weather.split('\n')
#     r = w[1].split(' | ')
#
#     return [w[0], r[0]]
#
#
# def get_current_weather_for_label():
#     weather_list = get_current_weather()
#     temperatureLabel.config(text='\n'.join(weather_list))
#     temperatureLabel.after(60000, get_current_weather_for_label)
#
#
# temperatureLabel = Label(root, font=("ds-digital", 35), background="black", foreground="cyan")
# temperatureLabel.place(x=550, y=250)
# get_current_weather_for_label()
#
# # End weather
# # Start News
#
# # End News
# # Start Tasks
# tasks = ['Done!', '30 min of Piano', '30 min of reading', 'Shower']
#
#
# def task_label(e):
#     text = tasks.pop()
#     if text != 'Done!' and len(tasks) != 0:
#         taskLabel.config(text=text)
#     else:
#         taskLabel.config(text=text)
#         tasks.append('Done!')
#     if e:
#         pass
#     else:
#         pass
#
#
# def add_to_list(label):
#     tasks.append(label.get())
#
#
# def popup_task():
#     window = Toplevel()
#
#     inputLabel = Entry(window)
#     Label(window, text="Task: ").grid(row=0)
#     inputLabel.grid(row=0, column=1)
#     Button(window,
#            text='Cancel',
#            command=window.destroy).grid(row=3,
#                                         column=0,
#                                         sticky=W,
#                                         pady=4)
#     Button(window,
#            text='Done', command=lambda: add_to_list(inputLabel)).grid(row=3,
#                                                                       column=1,
#                                                                       sticky=W,
#                                                                       pady=4)
#
#
# taskLabel = Label(root, font=("ds-digital", 30), background="black", foreground="cyan", cursor="hand2")
# taskLabel.place(x=215, y=400)
# taskLabel2 = Label(root, font=("ds-digital", 35), background="black", foreground="cyan", text="Tasks:")
# taskLabel2.place(x=200, y=350)
# task_label(True)
# taskLabel.bind('<Button-1>', lambda e: task_label(True))
#
# addTaskLabel = Label(root, font=("ds-digital", 30), background="black", foreground="green2", cursor="hand2",
#                      text="Add task")
#
# addTaskLabel.place(x=230, y=450)
# addTaskLabel.bind('<Button-1>', lambda e: popup_task())
# # End Tasks
# Start

mainloop()
