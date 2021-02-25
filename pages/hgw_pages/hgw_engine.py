# encoding: utf-8
# !/usr/bin/env python
# SaveTest
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
        pass

    def _init_driver(self):
        mobileEmulation = {'deviceName': 'iPhone X'}
        OPTIONS = webdriver.ChromeOptions()
        OPTIONS.add_argument('--ignore-certificate-errors')
        OPTIONS.add_experimental_option('mobileEmulation', mobileEmulation)
        self.DV = webdriver.Chrome(executable_path='chromedriver.exe', options=OPTIONS)
        width = self.DV.get_window_size().get("width")
        # self.DV.set_window_position(width/2, 0)
        self.DV.set_window_size(300, 814)

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
            self.homePage.open()
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
        if self.goHome():
            self.leaguesPage = self.homePage.goDay(day)
            if not self.leaguesPage:
                return False
        return False

        self.detailPage = self.leaguesPage.goLeague(homeName, awayName)
        if not self.detailPage:
            return False
        kof = self.detailPage.findLeagueKof(betType, betName, betParam)
        return kof

    def xiazhu(self, betType, betName, betParam, value):
        v = self.detailPage.onBet(betType, betName, betParam, value)
        return v

if __name__ == '__main__':
    hgwEngine = HgwEngine()
    hgwEngine.onInit()
    # hgwInit_thread = threading.Thread(target=hgwEngine.onInit)
    # hgwInit_thread.start()
    # print('hgwInit_thread start ing')
    # hgwInit_thread.join()
    # print('hgwInit_thread end')
