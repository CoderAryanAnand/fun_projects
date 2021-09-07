import tkinter as tk
from time import sleep
import pyglet

pyglet.font.add_file('who asks satan.ttf')

root = tk.Tk()
root.attributes('-fullscreen', True)
root.config(bg="black")

erebos_label = tk.Label(text="LYRIK: DER VERS", font=("who asks satan", 300), fg="red", bg="black")
# tritt_ein_label = tk.Label(text="TRITT EIN", font=("who asks satan", 150), fg="red", bg="black")
# kehr_um_label = tk.Label(text="KEHR UM", font=("who asks satan", 150), fg="red", bg="black")


def main():
    sleep(0.1)
    erebos_label.place(x=250, y=300)
    # tritt_ein_label.place(x=425, y=1000)
    # kehr_um_label.place(x=1575, y=1000)


root.after(100, main)
root.mainloop()
