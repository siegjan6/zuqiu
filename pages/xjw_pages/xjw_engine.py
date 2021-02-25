# encoding: utf-8
# !/usr/bin/env python
import time

from seleniumwire import webdriver

from pages.xjw_pages.xjw_login_page import XjwLoginPage
user = 'iceking666'
pwd = 'iceking666'
# user = 'siegjan'
# pwd = 'Zhouj5134'
url = 'https://m.uqmxd.com/account/login'

class XjwEngine():
    def __init__(self):
        pass

    def _init_driver(self):
        mobileEmulation = {'deviceName': 'iPhone X'}
        OPTIONS = webdriver.ChromeOptions()
        OPTIONS.add_argument('--ignore-certificate-errors')
        OPTIONS.add_experimental_option('mobileEmulation', mobileEmulation)
        self.DV = webdriver.Firefox(executable_path='geckodriver.exe', options=OPTIONS)
        self.DV.set_window_position(100, 0)
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
                return True
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
        return self.loginPage.goHome()

    def onInit(self):
        """初始化到登录后进入Home页"""
        self._init_driver()
        b = self.loginPage.open()
        if not b:  # 失败后间隔10秒重新初始化
            return False
        b = self._login(user, pwd)
        if not b:  # 失败后间隔10秒重新初始化
            return False
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