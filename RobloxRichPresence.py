# My Discord: d1n3x3z7
# My Github: https://github.com/d1n3x3z7
# My Discord Server: https://discord.gg/79P4Vew44D (тут можно помочь с разработкой, попросить помощи или просто найти друзей)
# version: 0.1.1

# Если у вас будет желание что-либо изменить в этом коде, помимо уже предстоящего, обращайтесь ко мне в дискорд
# Все баг репорты и пожелания в дискорд сервер

# Логика сканирования переработана

import pypresence

from time import sleep
from selenium import webdriver

from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchWindowException
from selenium.common.exceptions import WebDriverException

from bs4 import BeautifulSoup as bs

browser = webdriver.Chrome # можно изменять на Firefox/Chrome/Edge | else: (фу, ты что, пользуешься яндексом?)

browseroptions = Options()
browseroptions.add_argument('--no-sandbox')
browseroptions.page_load_strategy = 'normal'
browseroptions.add_experimental_option("excludeSwitches", ['enable-automation'])
browseroptions.add_argument('--log-level=3')

class RichPresence():

    def __init__(self):
        self.ssession = browser(options=browseroptions)
        self.ssession.maximize_window()

        browseroptions.add_argument('--headless')
        self.rsession = browser(options=browseroptions) # ну типо...

        self.presence = pypresence.Presence('1179993301718421585')

        self.state = 'Roblox Rich Presence'
        self.large_image = 'roblox'

        self.rblxcookie = None

        self.profilelink = None
        self.game = None
        self.gamelink = None
        self.joingamelink = None
        self.small_image = None
        self.details = None
        self.nickname = None

        self.start_session()
        while True:
            try:
                handler = self.ssession.window_handles
            except (NoSuchWindowException, WebDriverException):
                exit()

            self.update_status()

    def start_session(self):
        ss = self.ssession
        rs = self.rsession
        p = self.presence
        ss.get('https://www.roblox.com/Login')

        while ss.current_url == 'https://www.roblox.com/Login' or ss.current_url == 'https://www.roblox.com' or ss.current_url != 'https://www.roblox.com/home':
            continue
        
        p.connect()

        pars = bs(ss.page_source, 'html.parser')
        self.nickname = pars.find('span', class_='text-overflow age-bracket-label-username font-caption-header').text[0]
        self.profilelink = pars.find('a', class_='text-link dynamic-overflow-container')['href']

        cook = ss.get_cookie(name='.ROBLOSECURITY').get('value')
        rs.get('https://www.roblox.com/home')
        rs.add_cookie({'name':'.ROBLOSECURITY', 'value': cook, 'path':'/', 'domain':'.roblox.com','secure':True,'httpOnly':True})
        rs.refresh()
        rs.get(self.profilelink)
    
    def update_status(self):
        rs = self.rsession
        p = self.presence

        rs.refresh()
        sleep(1)
        rp = rs.page_source

        gs = bs(rp, 'html.parser')

        ingame = gs.find('span', class_='profile-avatar-status game icon-game')
        online = gs.find('span', class_='profile-avatar-status online icon-online')
        studio = gs.find('span', class_='profile-avatar-status studio icon-studio')

        if ingame == None and online == None and studio == None:
            self.details = 'Offline'
            p.update(state=self.state, details=self.details, large_image=self.large_image, buttons=[{'label': 'My Roblox Profile', 'url':self.profilelink}])
            return
        
        if ingame != None:
            self.game = ingame['title']
            self.gamelink = gs.find('a', class_='avatar-status')['href']
            self.details = f'Playing in {self.game}'
            p.update(state=self.state, details=self.details, large_image=self.large_image, buttons=[{'label': 'My Roblox Profile', 'url':self.profilelink},{'label':'Game', 'url':self.gamelink}])
            return
                
        if online != None:
            self.details = "Surfing the Roblox Website"

        if studio != None:
            self.details = 'Working in Roblox Studio'

        p.update(state=self.state, details=self.details, large_image=self.large_image, buttons=[{'label': 'My Roblox Profile', 'url':self.profilelink}])
        return

RichPresence()