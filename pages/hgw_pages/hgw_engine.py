# encoding: utf-8
# !/usr/bin/env python
# SaveTest
from seleniumwire import webdriver
import time
from pages.hgw_pages.hgw_login_page import HgwLoginPage

user = 'Zhouj5134'
pwd = 'Lpcaicai21'
url = 'https://205.201.4.166/'


class HgwEngine():
    def __init__(self):
        self.homePage = None

    def _init_driver(self):
        mobileEmulation = {'deviceName': 'iPhone X'}
        OPTIONS = webdriver.ChromeOptions()
        OPTIONS.add_argument('--ignore-certificate-errors')
        OPTIONS.add_experimental_option('mobileEmulation', mobileEmulation)
        self.DV = webdriver.Chrome(executable_path='chromedriver.exe', options=OPTIONS)
        self.loginPage = HgwLoginPage(self.DV, url)
        return True

    def _goDay(self, day):
        try:
            self.leaguesPage = self.homePage.goDay(user, pwd)
            if self.leaguesPage:
                return True
            else:
                False
        except:
            print('goday field')
            return False
        return True

    def login(self, u, p):
        try:
            self.homePage = self.loginPage.logIn(u, p)
            if self.homePage:
                return True
            else:
                return False
        except:
            print('login field')
            return False

    def quit(self):
        """
        退出
        :return:
        """
        self.DV.close()
        self.DV.quit()
        time.sleep(10)  # 10秒后重试，也可以指定时间重试

    def onInit(self):
        """初始化到登录后进入Home页"""
        self._init_driver()
        b = self.loginPage.open()
        if not b:  # 失败后间隔10秒重新初始化
            self.quit()
            return self.onInit()
        b = self.logIn(user, pwd)
        if not b:  # 失败后间隔10秒重新初始化
            self.quit()
            return self.onInit()
        return True

    def goHome(self):
        self.homePage.open()


loginPage.open()
homePage = loginPage.logIn(user, pwd)
leaguesPage = homePage.goDay(25)
# v = input('vv')
leaguesPage.saveData()

leaguesPage.driver.back()
leaguesPage.driver.back()
leaguesPage = homePage.goDay(26)
leaguesPage.saveData()

leaguesPage.driver.back()
leaguesPage.driver.back()
leaguesPage = homePage.goDay(27)
leaguesPage.saveData()

# leaguesPage.saveData()
# v = input('hhh')
# detailPage = leaguesPage.goLeague('利兹联队', '南安普顿')
# v = detailPage.onBet(18, '利兹联队', '-0.25', 10)
# k = 1
