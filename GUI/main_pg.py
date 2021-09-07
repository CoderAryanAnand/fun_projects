import pygame
import subprocess
import webbrowser
import time
import datetime

import requests
import wolframalpha
import os
import pygame_gui
from sys import argv

import psutil as psu

NAME = argv[0]


def system_info():
    info = {
        "Uptime": datetime.timedelta(seconds=time.time() - psu.boot_time()),
        "CPU in use": f"{psu.cpu_percent(interval=.1)}%",
        "Time on CPU": datetime.timedelta(seconds=psu.cpu_times().system + psu.cpu_times().user),
        "Memory in use": f"{psu.virtual_memory().percent}%",
        "Memory available": f"{psu.virtual_memory().available / (1024 ** 3):,.3f} GB",
        "Disk in use": f"{psu.disk_usage('/').percent}%",
        "Disk free": f"{psu.disk_usage('/').free / (1024 ** 3):,.3f} GB",
    }
    print("\n\n    SYSTEM INFO\n\n" + "\n".join([f"{key}: {value}" for key, value in info.items()]))


system_info()
pygame.init()
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1819, 1211
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("GUI")
manager = pygame_gui.UIManager((WIDTH, HEIGHT))

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
CYAN = (62, 254, 255)

TIME_FONT = pygame.font.Font(os.path.join('fonts', 'DS-DIGI.TTF'), 100)
MEMORY_FONT = pygame.font.Font(os.path.join('fonts', 'DS-DIGI.TTF'), 20)
CPU_FONT = pygame.font.Font(os.path.join('fonts', 'DS-DIGI.TTF'), 20)
DISK_FONT = pygame.font.Font(os.path.join('fonts', 'DS-DIGI.TTF'), 20)
MEM_AVA_FONT = pygame.font.Font(os.path.join('fonts', 'DS-DIGI.TTF'), 20)

FPS = 60

BG = pygame.image.load(os.path.join('images', 'bg1.png'))
WIN.blit(BG, (0, 0))

CMD_IMAGE = pygame.transform.scale(pygame.image.load('images/cmd.png'), (100, 70))
YOUTUBE_IMAGE = pygame.transform.scale(pygame.image.load('images/Youtube.png'), (100, 70))
GITHUB_IMAGE = pygame.transform.scale(pygame.image.load('images/Github.png'), (70, 70))
GMAIL_IMAGE = pygame.transform.scale(pygame.image.load('images/Gmail.png'), (100, 74))
WHATSAPP_IMAGE = pygame.transform.scale(pygame.image.load('images/Whatsapp.png'), (75, 75))
MINECRAFT_IMAGE = pygame.transform.scale(pygame.image.load('images/Minecraft block.png'), (72, 80))


class Button:
    def __init__(self, image, position, callback):
        self.image = image
        self.rect = image.get_rect(topleft=position)
        self.callback = callback

    def on_click(self, event):
        if event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.callback(self)


def open_(name):
    if name == 'wa':
        subprocess.Popen(["cmd", "/C", "start whatsapp://send?phone=0041779094359^&text=Hello"], shell=True)
    elif name == 'yt':
        webbrowser.open("https://www.youtube.com/")
    elif name == 'mc':
        subprocess.run(r"C:\Program Files (x86)\Minecraft Launcher\MinecraftLauncher.exe")
    elif name == 'gh':
        webbrowser.open("https://www.github.com/")
    elif name == 'gm':
        webbrowser.open("https://mail.google.com/mail/u/0/#inbox")
    elif name == 'cmd':
        subprocess.run("wt.exe")


def hovering_on_shortcut(x, y, buttons):
    cmdButton, youtubeButton, githubButton, gmailButton, minecraftButton, whatsappButton = buttons[0], buttons[1], \
                                                                                           buttons[2], buttons[3], \
                                                                                           buttons[4], buttons[5]
    return (x in range(500, cmdButton.rect.right)) and (y in range(400, cmdButton.rect.bottom)) or (
            x in range(cmdButton.rect.right + 20, youtubeButton.rect.right)) and (
                   y in range(400, youtubeButton.rect.bottom)) or (
                   x in range(youtubeButton.rect.right + 20, githubButton.rect.right)) and (
                   y in range(400, githubButton.rect.bottom)) or (
                   x in range(githubButton.rect.right + 20, gmailButton.rect.right)) and (
                   y in range(400, gmailButton.rect.bottom)) or (
                   x in range(gmailButton.rect.right + 20, minecraftButton.rect.right)) and (
                   y in range(400, minecraftButton.rect.bottom)) or (
                   x in range(minecraftButton.rect.right + 20, whatsappButton.rect.right)) and (
                   y in range(400, whatsappButton.rect.bottom))


def draw_window(buttons):
    WIN.blit(BG, (0, 0))

    manager.draw_ui(WIN)
    # time
    digital_text = datetime.datetime.now().strftime('%H:%M:%S')
    text = TIME_FONT.render(digital_text, True, CYAN)  # 714 41, 1106 165
    text_rect = text.get_rect(center=((392 / 2) + 714, (124 / 2) + 41))
    WIN.blit(text, text_rect)

    # CPU + Memory
    cpu_in_use = f"CPU usage: {psu.cpu_percent(interval=.1)}%"
    mem_in_use = f"RAM usage: {psu.virtual_memory().percent}%"
    mem_ava = f"RAM free: {psu.virtual_memory().available / (1024 ** 3):,.3f} GB"
    disk_ava = f"Disk space free: {psu.disk_usage('/').free / (1024 ** 3):,.3f} GB"

    cpu = psu.cpu_percent()
    mem = psu.virtual_memory().percent
    vir_mem_ava = psu.virtual_memory().available / (1024 ** 3)
    disk = psu.disk_usage('/').free / (1024 ** 3)

    if 100 > cpu > 70:
        text_cpu_in_use = CPU_FONT.render(cpu_in_use, True, YELLOW)
    else:
        text_cpu_in_use = CPU_FONT.render(cpu_in_use, True, CYAN)
    if 100 > mem > 70:
        text_mem_in_use = MEMORY_FONT.render(mem_in_use, True, YELLOW)
    else:
        text_mem_in_use = MEMORY_FONT.render(mem_in_use, True, CYAN)
    if 100 > disk > 70:
        text_disk_in_use = DISK_FONT.render(disk_ava, True, YELLOW)
    else:
        text_disk_in_use = DISK_FONT.render(disk_ava, True, CYAN)
    if 100 > vir_mem_ava > 70:
        text_mem_ava = MEM_AVA_FONT.render(mem_ava, True, YELLOW)
    else:
        text_mem_ava = MEM_AVA_FONT.render(mem_ava, True, CYAN)

    cpu_rect = text_cpu_in_use.get_rect(center=((205 / 2) + 33, (23 / 2) + 50))  # (33, 50), (238, 73)
    mem_use_rect = text_mem_in_use.get_rect(center=((205 / 2) + 252, (23 / 2) + 50))  # (252, 50), (457, 73)
    mem_ava_rect = text_mem_ava.get_rect(center=((205 / 2) + 472, (23 / 2) + 50))  # (472, 50), (677, 73)
    disk_rect = text_disk_in_use.get_rect(center=((205 / 2) + 1165, (23 / 2) + 50))  # (1155, 50), (1360, 73)

    WIN.blit(text_disk_in_use, disk_rect)
    WIN.blit(text_mem_in_use, mem_use_rect)
    WIN.blit(text_cpu_in_use, cpu_rect)
    WIN.blit(text_mem_ava, mem_ava_rect)

    # Shortcuts
    for i in buttons:
        WIN.blit(i.image, i.rect)

    # Weather

    pygame.display.flip()

    pygame.display.update()


def main():
    clock = pygame.time.Clock()
    is_running = True
    # Shortcuts
    # Define and create button
    cmdButton = Button(CMD_IMAGE, (500, 400),
                       lambda e: open_('cmd'))
    youtubeButton = Button(YOUTUBE_IMAGE,
                           (cmdButton.rect.right + 20, 400),
                           lambda e: open_('yt'))
    githubButton = Button(GITHUB_IMAGE,
                          (youtubeButton.rect.right + 20, 400),
                          lambda e: open_('gh'))
    gmailButton = Button(GMAIL_IMAGE,
                         (githubButton.rect.right + 20, 400),
                         lambda e: open_('gm'))
    minecraftButton = Button(MINECRAFT_IMAGE,
                             (gmailButton.rect.right + 20, 400),
                             lambda e: open_('mc'))
    whatsappButton = Button(WHATSAPP_IMAGE,
                            (minecraftButton.rect.right + 20, 400),
                            lambda e: open_('wa'))
    buttons = [cmdButton, youtubeButton, githubButton,
               gmailButton, minecraftButton, whatsappButton]

    while is_running:
        time_delta = clock.tick(FPS)
        # time.sleep(1)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    button.on_click(event)
                print(pygame.mouse.get_pos())
            if event.type == pygame.MOUSEBUTTONUP:
                print(pygame.mouse.get_pos())
            # if event.type == pygame.USEREVENT:
            #     if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
            #         if event.ui_element == hello_button:
            #             print('Hello World!')

            manager.process_events(event)

        x_y_coords = list(pygame.mouse.get_pos())
        if hovering_on_shortcut(x_y_coords[0], x_y_coords[1], buttons):
            pygame.mouse.set_cursor(*pygame.cursors.tri_left)
        else:
            pygame.mouse.set_cursor(*pygame.cursors.arrow)
        manager.update(time_delta)
        draw_window(buttons)


if __name__ == '__main__':
    main()
