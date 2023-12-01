# My Discord: d1n3x3z7
# My Github: https://github.com/Denixuz
# My Discord Server: https://discord.gg/79P4Vew44D (тут можно помочь с разработкой, попросить помощи или просто найти друзей)
# version: 0.1.0

# Если у вас будет желание что-либо изменить в этом коде, помимо уже предстоящего, обращайтесь ко мне в дискорд
# Все баг репорты и пожелания в дискорд сервер

# Вообщем, на данный момент софт обрабатывает всё по тупой логике, что в следующих обновлениях будет изменено
# RRP не видит игру если вы не входили в неё через страницу самой игры + рипается показ игры если вы перейдёте на другую страницу (это будет изменено)

import pypresence
import psutil

from selenium import webdriver

from selenium.webdriver.chrome.options import Options

from bs4 import BeautifulSoup as bs

browseroptions = Options()
browseroptions.add_argument('--no-sandbox')
browseroptions.page_load_strategy = 'normal'

class RichPresence():

    def __init__(self):
        self.session = webdriver.Chrome(options=browseroptions)
        self.presence = pypresence.Presence('1179993301718421585')
        self.profilelink = None
        self.game = None
        self.gamelink = None
        self.joingamelink = None
        self.large_image = 'roblox'
        self.small_image = None
        self.state = 'RRP Alpha'
        self.details = None
        self.nickname = None

        self.start_session()
        while True:
            self.update_status()

    def start_session(self):
        s = self.session
        p = self.presence
        s.get('https://www.roblox.com/Login')

        while s.current_url == 'https://www.roblox.com/Login' or s.current_url == 'https://www.roblox.com':
            continue
        
        p.connect()
        pars = bs(s.page_source, 'html.parser')
        self.nickname = pars.find('span', class_='text-overflow age-bracket-label-username font-caption-header').text[0]
        self.profilelink = pars.find('a', class_='text-link dynamic-overflow-container')['href']
        self.state = 'nothing...'
        self.details = 'Idling'

    
    def update_status(self):
        s = self.session
        p = self.presence

        gamelaunched = False

        for x in psutil.process_iter():
            if x.name == 'RobloxPlayerBeta.exe':
                gamelaunched = True

        if 'https://www.roblox.com/games/' in s.current_url and gamelaunched == True:
            if '#' in s.current_url:
                self.game = ''.join(s.current_url[s.current_url[:s.current_url.find('#')].rfind('/')+1:].split('-'))
                self.gamelink = s.current_url[:s.current_url.find('#')]
            else:
                self.game = ''.join(s.current_url[s.current_url.rfind('/')+1:].split('-'))
                self.gamelink = s.current_url
            
            self.details = f'Playing in {self.game}'

            p.update(state=self.state, details=self.details, large_image=self.large_image, buttons=[{'label': 'My Roblox Profile', 'url':self.profilelink},{'label':'Game', 'url':self.gamelink}])
        else:
            self.details = 'Idling'
            p.update(state=self.state, details=self.details, large_image=self.large_image, buttons=[{'label': 'My Roblox Profile', 'url':self.profilelink}])

RichPresence()