# encoding: utf-8
# !/usr/bin/env python
from seleniumwire import webdriver

from pages.xjw_pages.xjw_login_page import XjwLoginPage
user = 'iceking666'
pwd = 'iceking666'
url = 'https://m.uqmxd.com/account/login'

mobileEmulation = {'deviceName': 'iPhone X'}
OPTIONS = webdriver.ChromeOptions()
OPTIONS.add_argument('--ignore-certificate-errors')
OPTIONS.add_experimental_option('mobileEmulation', mobileEmulation)
DV = webdriver.Chrome(executable_path='chromedriver.exe', options=OPTIONS)

loginPage = XjwLoginPage(DV, url)
loginPage.open()
gameListPage = loginPage.logIn(user, pwd)
homePage = gameListPage.goNextPage()
leaguesPage = homePage.goDay(False)
data = leaguesPage.saveData()
print(data)