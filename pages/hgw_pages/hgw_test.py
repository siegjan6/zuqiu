# encoding: utf-8
# !/usr/bin/env python
# SaveTest
from seleniumwire import webdriver

import datetime
from pages.hgw_pages.hgw_login_page import HgwLoginPage

user = 'Zhouj5134'
pwd = 'Lpcaicai21'
url = 'https://205.201.4.166/'

mobileEmulation = {'deviceName': 'iPhone X'}
OPTIONS = webdriver.ChromeOptions()
OPTIONS.add_argument('--ignore-certificate-errors')
OPTIONS.add_experimental_option('mobileEmulation', mobileEmulation)
DV = webdriver.Chrome(executable_path='chromedriver.exe', options=OPTIONS)

loginPage = HgwLoginPage(DV, url)
loginPage.open()
homePage = loginPage.login(user, pwd)

day = 1#datetime.datetime.now().day
for i in range(5):
    leaguesPage = homePage.goDay(day)
    if leaguesPage:
        leaguesPage.saveData()
        leaguesPage.driver.back()
        leaguesPage.driver.back()
        day = day+1



#leaguesPage.saveData()
# v = input('hhh')
# detailPage = leaguesPage.goLeague('利兹联队', '南安普顿')
# v = detailPage.onBet(18, '利兹联队', '-0.25', 10)
# k = 1