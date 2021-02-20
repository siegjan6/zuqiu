# encoding: utf-8
# !/usr/bin/env python

from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC  # available since 2.26.0
from selenium.webdriver.common.touch_actions import TouchActions
# from browsermobproxy import Server

from selenium.webdriver.common.keys import Keys
from time import sleep
from datetime import timedelta
import datetime
import time


def interceptor(request, response):
    print(request.path)
    # if request.method == 'POST' and request.path =='/transform.php':
    #     if response.headers['Content-Type'] == 'text/xml':
    #         print(response)


def getBetTypeName(typeNum):
    if typeNum == 17:
        return ['让球', 'head_R_FT_', 'body_R_FT_']
    if typeNum == 18:
        return ['让球', 'head_R_FT_', 'body_R_FT_']
    if typeNum == 19:
        return ['大 / 小', 'head_OU_FT_', 'body_OU_FT_']
    if typeNum == 20:
        return ['大 / 小', 'head_OU_FT_', 'body_OU_FT_']


def updatePank(ary):
    l = len(ary)
    for i in range(l):
        x = ary[i]
        if x.find('/') != -1:
            r = x.split('/')
            x = (float(r[0]) + float(r[1])) / 2
            ary[i] = str(x)
    return ary


class HgwRequest:
    def __init__(self):
        self._timeout = 20
        self._usr = 'Zhouj5134'
        self._pwd = 'Lpcaicai21'
        mobileEmulation = {'deviceName': 'iPhone X'}
        self.OPTIONS = webdriver.ChromeOptions()
        self.OPTIONS.add_argument('--ignore-certificate-errors')
        self.OPTIONS.add_experimental_option('mobileEmulation', mobileEmulation)
        self.DV = webdriver.Chrome(executable_path='chromedriver.exe', options=self.OPTIONS)

        def req_inter(request):
            del request.headers['referer']
            request.headers['referer'] = "https://www.test.com"

        self.DV.request_interceptor = req_inter
        # self.DV.response_interceptor = interceptor

    def openLoginPage(self):

        self.DV.get('http://205.201.4.166/')
        try:
            element1 = WebDriverWait(self.DV, self._timeout).until(EC.presence_of_element_located((By.ID, "usr")))
            element2 = WebDriverWait(self.DV, self._timeout).until(EC.presence_of_element_located((By.ID, "pwd")))
        except:
            print('找不到登录页面的元素，或者网站登录页面打开超时')
            self.DV.close()
        finally:
            print('打开登录页面完毕')

    def _clicknobtn(self):
        element2 = WebDriverWait(self.DV, self._timeout).until(EC.element_to_be_clickable((By.ID, 'no_btn')))
        self.DV.find_element_by_id('no_btn').click()

    def _checkOkBtn(self):  #
        if WebDriverWait(self.DV, self._timeout).until(EC.element_to_be_clickable((By.ID, 'ok_btn'))):
            self.DV.find_element_by_id('ok_btn').click()
        sleep(1)

    def pushUsrPwd(self):
        self.DV.find_element_by_id('usr').send_keys(self._usr)
        self.DV.find_element_by_id('pwd').send_keys(self._pwd)
        self.DV.find_element_by_id('btn_login').click()
        try:
            element1 = WebDriverWait(self.DV, self._timeout).until(EC.presence_of_element_located((By.ID, "no_btn")))
        except:
            print('登录后未发现no_btn元素，或者超时')
            self.DV.close()
        finally:
            print('登录1完毕')

    def logOut(self):
        self.DV.find_element_by_id('myAcc_page').click()
        sleep(1)
        self.DV.find_element_by_class_name('btn_logout').click()
        sleep(1)
        self.DV.close()

    # 打开网址到登录完毕
    def login(self):
        self.openLoginPage()
        self.pushUsrPwd()
        self._clicknobtn()
        sleep(5)
        element2 = WebDriverWait(self.DV, self._timeout).until(EC.element_to_be_clickable((By.ID, 'ft_live_league')))

    # 简单比对一下日期，后期细化
    def isToDay(self, t):
        now = datetime.datetime.now()
        d1 = now.day
        d2 = time.localtime(t).tm_mday
        return d1 == d2

    def updateTime(self, t):
        interval = timedelta(hours=-12)
        d = datetime.datetime.fromtimestamp(t)
        d = d + interval
        return d.timestamp()


    def onClickToDay(self):
        self.DV.find_element_by_id('today_page').click()
        sleep(2)
        element2 = WebDriverWait(self.DV, self._timeout).until(EC.element_to_be_clickable((By.ID, 'btn_coupon1')))
        self.DV.find_element_by_id('btn_coupon1').click()
        sleep(5)

    def onClickToEarly(self, day):
        day = str(time.localtime(day).tm_mday)
        self.DV.find_element_by_id('early_page').click()
        sleep(3)
        element2 = WebDriverWait(self.DV, self._timeout).until(EC.element_to_be_clickable((By.ID, 'date_icon')))
        self.DV.find_element_by_id('date_icon').click()
        sleep(0.5)
        elements = self.DV.find_elements_by_class_name('btn_date')
        for e in elements:
            ary = e.text.split('\n')
            if len(ary) == 3 and ary[1] == day:
                e.click()
                sleep(1)
                element2 = WebDriverWait(self.DV, self._timeout).until(
                    EC.element_to_be_clickable((By.ID, 'div_coupon')))
                sleep(1)
                self.DV.find_element_by_id('btn_coupon1').click()
                sleep(6)
                return True
        return False

    # 具体比赛页面，寻找具体口水
    def findDetial(self, data):
        betType = getBetTypeName(data['bet_type_name'])
        css_selector = 'div[id*=' + betType[2] + ']'
        element_betTypes = self.DV.find_elements_by_css_selector(css_selector)  # 口水数组
        for e in element_betTypes:
            ary = e.text.split('\n')
            ary = updatePank(ary)
            print(ary)
            if data['market_and_bet_type'] == 17:
                if ary[0] == data['bet_name'] and ary[1] == str(data['market_and_bet_type_param']):
                    return [e, ary[4]]
            elif data['market_and_bet_type'] == 18:
                fpank = ary[1]
                if ary[1] != '0':
                    fpank = '-' + ary[1]

                if ary[3] == data['bet_name'] and fpank == str(data['market_and_bet_type_param']):
                    return [e, ary[4]]
            if data['market_and_bet_type'] == 19:  # 大
                if ary[1] == str(data['market_and_bet_type_param']):
                    return [e, ary[2]]
            elif data['market_and_bet_type'] == 20:  # 小
                if ary[4] == str(data['market_and_bet_type_param']):
                    return [e, ary[5]]
        # 到这里 就说明未找到对应的口水
        print('未找到比赛对应的口水')
        print('数据网数据', data)
        return None

    def findLeague(self, data, bClick = True):
        data['started_at'] = self.updateTime(data['started_at'])
        if self.isToDay(data['started_at']):
            self.onClickToDay()
        else:
            self.onClickToEarly(data['started_at'])

        element2 = WebDriverWait(self.DV, self._timeout).until(EC.element_to_be_clickable((By.ID, 'tab_main')))
        element2.click()
        sleep(3)
        # els = self.DV.find_elements_by_class_name('btn_inn_team')

        # 向下滚动找比赛
        element_new = self.DV.find_element_by_tag_name('html')
        _leagues = {}
        l = -1
        while len(_leagues) != l:
            l = len(_leagues)
            element_new.send_keys(Keys.ARROW_DOWN * 40)
            sleep(1)
            els = self.DV.find_elements_by_class_name('btn_inn_team')
            length = len(els)
            for i in range(length):
                try:
                    e = els[i]
                    print(e)
                    ary = e.text.split('\n')
                    if len(ary) < 2:
                        continue
                    _leagues[ary[0]] = ary[1]
                    homeName = ary[0]
                    awayName = ary[1]
                    print(homeName, awayName)
                    if homeName == data['home'] and awayName == data['away']:
                        if bClick:
                            e.click()
                            sleep(0.5)
                            WebDriverWait(self.DV, self._timeout).until(EC.element_to_be_clickable((By.ID, 'team_h')))
                            sleep(0.5)
                            return True
                        break
                except ValueError:
                    continue
        # 到这里说明未找到比赛
        d2 = time.localtime(data['started_at']).tm_mday
        print('该日期下未找到比赛：请找到比赛，核对日期和名字')
        print('数据网站日期', d2)
        print('数据网队伍', data['home'], data['away'])
        print('页面中的队伍', _leagues)
        return None

    def findLeagueToDetail(self, data):
        e = self.findLeague(data)  # 找到具体比赛，返回 比赛element
        if e:
            # e.click()
            es = self.findDetial(data)
            return es
        return None




if __name__ == '__main__':
    hgw = HgwRequest()
    hgw.login()
    while True:
        sleep(1)
