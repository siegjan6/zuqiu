# encoding: utf-8
# !/usr/bin/env python
from seleniumwire import webdriver

from pages.xjw_pages.xjw_login_page import XjwLoginPage
# user = 'iceking666'
# pwd = 'iceking666'
user = 'siegjan'
pwd = 'Zhouj5134'
url = 'https://m.uqmxd.com/account/login'

mobileEmulation = {'deviceName': 'iPhone X'}
OPTIONS = webdriver.ChromeOptions()
OPTIONS.add_argument('--ignore-certificate-errors')
OPTIONS.add_experimental_option('mobileEmulation', mobileEmulation)
DV = webdriver.Chrome(executable_path='chromedriver.exe', options=OPTIONS)

loginPage = XjwLoginPage(DV, url)
loginPage.open()
homePage = loginPage.login(user, pwd)
leaguesPage = homePage.goDay(True)
leaguesPage.saveData()
leaguesPage.driver.back()
leaguesPage = homePage.goDay(False)
leaguesPage.saveData()
# v = input('hhh')
# detailPage = leaguesPage.goLeague('利兹联队', '南安普顿')
# v = detailPage.onBet(18, '利兹联队', '-0.25', 10)
# k = 1