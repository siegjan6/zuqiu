# encoding: utf-8
# !/usr/bin/env python
# SaveTest
import datetime
import threading

from seleniumwire import webdriver
import time
from pages.hgw_pages.hgw_login_page import HgwLoginPage

user = 'Zhouj5134'
pwd = 'Lpcaicai21'
url = 'https://205.201.4.166/'


class HgwEngine():
    def __init__(self):
        self.is_init = False
        self.koef = None
        self.isErrLeague= {}
        self.home_url = None
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
        self.koef = None
        self.is_init = None
        mobileEmulation = {'deviceName': 'iPhone X'}
        OPTIONS = webdriver.ChromeOptions()
        OPTIONS.add_argument('--ignore-certificate-errors')
        OPTIONS.add_experimental_option('mobileEmulation', mobileEmulation)
        self.DV = webdriver.Chrome(executable_path='chromedriver.exe', options=OPTIONS)
        width = self.DV.get_window_size().get("width")
        height = self.DV.get_window_size().get("height")
        self.DV.set_window_position(0, 0)
        self.DV.set_window_size(375, height)

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

    def _login(self, u, p):
        try:
            self.homePage = self.loginPage.login(u, p)
            if self.homePage:
                self.home_url = self.homePage.driver.current_url
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
        if self.homePage:
            self.homePage.driver.get(self.home_url)
            return True
        return False

    def onInit(self):
        """初始化到登录后进入Home页"""
        self._init_driver()
        b = self.loginPage.open()
        if not b:
            self.is_init = False
            return False
        self.homePage = self._login(user, pwd)
        if not b:
            self.is_init = False
            return False
        self.is_init = True
        return True

    def getKof(self, day, homeName, awayName, betType, betName, betParam):
        if self.isErrorLeague(homeName, awayName):
            self.koef = None
            return False

        # if self.goHome():
        self.leaguesPage = self.homePage.goDay(day)
        if not self.leaguesPage:
            return False

        self.detailPage = self.leaguesPage.goLeague(homeName, awayName)
        if not self.detailPage:
            return False
        self.koef = self.detailPage.findLeagueKof(betType, betName, betParam)
        if not self.koef:
            self.addErrorLeague(homeName, awayName)
        return self.koef

    def xiazhu(self, betType, betName, betParam, value):
        v = self.detailPage.onBet(betType, betName, betParam, value)
        return v

    def threading_init(self):
        t = threading.Thread(target=self.onInit)
        t.setDaemon(True)
        t.start()
        return t

    def threading_getkoef(self, d):
        homeName = d['hgw']['home']
        awayName = d['hgw']['away']
        time = d['hgw']['started_at']
        kof = d['hgw']['koef']
        betType = d['hgw']['bet_type_name']
        betParam = d['hgw']['market_and_bet_type_param']
        betName = d['hgw']['bet_name']

        dt = datetime.datetime.fromtimestamp(time)
        day = dt.day
        t = threading.Thread(target=self.getKof, args=(day, homeName, awayName, betType, betName, betParam))
        t.setDaemon(True)
        t.start()
        return t


if __name__ == '__main__':
    hgwEngine = HgwEngine()
    hgwEngine.onInit()
    # hgwInit_thread = threading.Thread(target=hgwEngine.onInit)
    # hgwInit_thread.start()
    # print('hgwInit_thread start ing')
    # hgwInit_thread.join()
    # print('hgwInit_thread end')
