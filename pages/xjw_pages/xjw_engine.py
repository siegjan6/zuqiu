# encoding: utf-8
# !/usr/bin/env python
import threading
import time
import datetime
from seleniumwire import webdriver

from pages.xjw_pages.xjw_login_page import XjwLoginPage
user = 'iceking666'
pwd = 'iceking666'
# user = 'siegjan'
# pwd = 'Zhouj5134'
url = 'https://m.uqmxd.com/account/login'

class XjwEngine():
    def __init__(self):
        self.is_init = False
        self.koef = None
        self.isErrLeague= {}
        pass

    def addErrorLeague(self, home, away):
        if home + away in self.isErrLeague:
            self.isErrLeague[home + away] = self.isErrLeague[home + away] + 1
        else:
            self.isErrLeague[home + away] = 1

    def isErrorLeague(self, home, away):
        if home + away in self.isErrLeague:
            return self.isErrLeague[home + away]
        else:
            return None

    def _init_driver(self):
        self.is_init = False
        self.koef = None
        mobileEmulation = {'deviceName': 'iPhone X'}
        OPTIONS = webdriver.ChromeOptions()
        OPTIONS.add_argument('--ignore-certificate-errors')
        OPTIONS.add_experimental_option('mobileEmulation', mobileEmulation)
        self.DV = webdriver.Chrome(executable_path='chromedriver.exe', options=OPTIONS)
        width = self.DV.get_window_size().get("width")
        height = self.DV.get_window_size().get("height")
        self.DV.set_window_position(width / 2, 0)
        self.DV.set_window_size(375, height)
        self.loginPage = XjwLoginPage(self.DV, url)
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

    def _login(self, u, p):
        try:
            self.homePage = self.loginPage.login(u, p)
            if self.homePage:
                return self.homePage
            else:
                return False
        except:
            print('_login field')
            return False

    def _quit(self):
        """
        退出
        :return:
        """
        self.DV.close()
        self.DV.quit()
        time.sleep(5)  # 10秒后重试，也可以指定时间重试

    def goHome(self):
        try:
            if self.loginPage:
                self.loginPage.goHome()
            return True
        except:
            return False

    def onInit(self):
        """初始化到登录后进入Home页"""
        self._init_driver()
        b = self.loginPage.open()
        if not b:
            self.is_init = False
            return False
        self.homePage = self._login(user, pwd)
        if not self.homePage:
            self.is_init = False
            return False
        self.is_init = True
        return True

    def getKof(self, day, homeName, awayName, betType, betName, betParam):
        if self.isErrorLeague(homeName, awayName):
            self.koef = None
            return False
        self.loginPage.goHome()
        isToDay = datetime.datetime.now().day == day
        self.leaguesPage = self.homePage.goDay(isToDay)
        if not self.leaguesPage:
            return False

        self.detailPage = self.leaguesPage.goLeague(homeName, awayName)
        if not self.detailPage:
            return False
        self.koef = self.detailPage.findLeagueKof(betType, betName, betParam)
        if not self.koef:
            self.addErrorLeague(homeName, awayName)
        return self.koef

    def xiazhu(self, d, value):
        homeName = d['xjw']['home']
        awayName = d['xjw']['away']
        time = d['xjw']['started_at']
        kof = d['xjw']['koef']
        betType = d['xjw']['bet_type_name']
        betParam = d['xjw']['market_and_bet_type_param']
        betName = d['xjw']['bet_name']
        v = self.detailPage.onBet(betType, betName, betParam, value)
        return v

    def threading_init(self):
        t = threading.Thread(target= self.onInit)
        t.setDaemon(True)
        t.start()
        return t

    def threading_getkoef(self, d):
        homeName = d['xjw']['home']
        awayName = d['xjw']['away']
        time = d['xjw']['started_at']
        kof = d['xjw']['koef']
        betType = d['xjw']['bet_type_name']
        betParam = d['xjw']['market_and_bet_type_param']
        betName = d['xjw']['bet_name']

        dt = datetime.datetime.fromtimestamp(time)
        day = dt.day
        t = threading.Thread(target=self.getKof, args=(day, homeName, awayName, betType, betName, betParam))
        t.setDaemon(True)
        t.start()
        return t

if __name__ == '__main__':
    xjwEngine = XjwEngine()
    v = xjwEngine.onInit()
    if v:
        kof = xjwEngine.getKof(25, '罗勇', '巴吞联', 17, '罗勇', 2)
        if kof:
            v = xjwEngine.xiazhu(17, '罗勇', '2', 20)
            print(v)
    else:
        xjwEngine.goHome()


# v = input('hhh')
# detailPage = leaguesPage.goLeague('利兹联队', '南安普顿')
# v = detailPage.onBet(18, '利兹联队', '-0.25', 10)
# k = 1