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
    pass
    # if typeNum == 17:
    #     return ['让球', 'head_R_FT_', 'body_R_FT_']
    # if typeNum == 18:
    #     return ['让球', 'head_R_FT_', 'body_R_FT_']
    # if typeNum == 19:
    #     return ['大 / 小', 'head_OU_FT_', 'body_OU_FT_']
    # if typeNum == 20:
    #     return ['大 / 小', 'head_OU_FT_', 'body_OU_FT_']


def updatePank(ary):
    pass
    # l = len(ary)
    # for i in range(l):
    #     x = ary[i]
    #     if x.find('/') != -1:
    #         r = x.split('/')
    #         x = (float(r[0]) + float(r[1])) / 2
    #         ary[i] = str(x)
    # return ary


class XjwRequest:
    def __init__(self):
        self._timeout = 20
        self._usr = 'siegjan'
        self._pwd = 'Zhouj5134'
        mobileEmulation = {'deviceName': 'iPhone X'}
        self.OPTIONS = webdriver.ChromeOptions()
        self.OPTIONS.add_argument('--ignore-certificate-errors')
        self.OPTIONS.add_experimental_option('mobileEmulation', mobileEmulation)
        self.DV = webdriver.Chrome(executable_path='chromedriver.exe', options=self.OPTIONS)

        def req_inter(request):
            # Block PNG, JPEG and GIF images
            if request.path.endswith(('.png', '.jpg', '.gif')):
                request.abort()

        self.DV.request_interceptor = req_inter
        # self.DV.response_interceptor = interceptor

    def openLoginPage(self):
        try:
            self.DV.get('http://11mx.cc')
            sleep(5)
            element1 = WebDriverWait(self.DV, self._timeout).until(
                EC.presence_of_element_located((By.CLASS_NAME, "no-acc-path")))

        except:
            print('找不到登录页面的元素，或者网站登录页面打开超时')
            self.DV.close()
            self.openLoginPage()
            return False
        finally:
            print('打开登录页面完毕')
        return True

    def _clicknoaccpath(self):
        element1 = WebDriverWait(self.DV, self._timeout).until(
            EC.presence_of_element_located((By.CLASS_NAME, "no-acc-path")))
        element1.click()  # 点击已有账号，登录
        sleep(1)
        WebDriverWait(self.DV, self._timeout).until(EC.presence_of_element_located((By.ID, "uid")))

    def _checkOkBtn(self):  #
        if WebDriverWait(self.DV, self._timeout).until(EC.element_to_be_clickable((By.ID, 'ok_btn'))):
            self.DV.find_element_by_id('ok_btn').click()
        sleep(1)

    def pushUsrPwd(self):
        self.DV.find_element_by_id('uid').send_keys(self._usr)
        self.DV.find_element_by_id('jpwd').send_keys(self._pwd)
        sleep(3)
        self.DV.find_element_by_id('gologin').click()
        # 这里出现验证码 class
        try:
            WebDriverWait(self.DV, self._timeout).until(EC.presence_of_element_located((By.CLASS_NAME, "popup-wrap")))
            sleep(10)  # 这秒内完成验证码验证
            WebDriverWait(self.DV, self._timeout).until(
                EC.presence_of_element_located((By.ID, "gamelist")))  # 可能存在问题，数据还未加载完，gamelist提早存在

        except:
            print('登录后未发现验证码验证元素，或者超时')
            self.DV.close()
        finally:
            print('登录1完毕')

    def backOldVersion(self):
        self.DV.find_element_by_class_name('ab-a').find_element_by_xpath('//div//div[5]').click()
        sleep(1)
        self.DV.find_element_by_class_name('text-with-badge').click()  # 回到先前版本
        sleep(2)
        WebDriverWait(self.DV, self._timeout).until(
            EC.presence_of_element_located((By.CLASS_NAME, "icon-arrow-bottom")))

    def openYazhou(self):
        continue_link = self.DV.find_element_by_link_text('亚洲体育')
        continue_link.click()
        sleep(3)
        # 弹出新页面 ,进入新页面（亚洲体育）
        self.DV.switch_to_window(self.DV.window_handles[1])
        sleep(1)
        e = WebDriverWait(self.DV, self._timeout).until(EC.presence_of_element_located((By.CLASS_NAME, "btn-reset")))
        e.click()  # 这之后有可能加载不出来。 进入亚洲首页
        print('openYazhou End')
        # WebDriverWait(self.DV, self._timeout).until(EC.presence_of_element_located((By.CLASS_NAME, "pl-c__menu")))  # 可能存在问题
        # self._baseURL = self.DV.current_url

    # 打开网址到登录完毕
    def login(self):
        b = self.openLoginPage()
        if not b:
            return b
        self._clicknoaccpath()
        self.pushUsrPwd()
        self.openYazhou()
        sleep(10)
        # self.backOldVersion()
        print('初始化完毕')

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

    def wait_refresh(self, dd):
        isOK = EC.element_to_be_clickable(By.ID, dd)
        print(isOK)
        index = 0
        while not isOK:
            index = index + 1
            if index % 8 == 0:
                self.DV.refresh()
            sleep(3)
            isOK = EC.element_to_be_clickable(By.ID, '1_t')
            print(isOK)

    def onClickToDay(self):  # 今日
        self.DV.find_element_by_class_name('pl-c__menu').find_elements_by_class_name('pl-c__btn')[0].click()
        sleep(0.5)
        self.DV.find_element_by_class_name('pl-c__col').find_elements_by_class_name('pl-c__game')[0].click()
        sleep(5)
        # 此处需要等待
        print('onClickToDay End')

    def onClickToEarly(self, day):  # 早盘
        self.DV.find_element_by_class_name('pl-c__menu').find_elements_by_class_name('pl-c__btn')[1].click()
        sleep(0.5)
        self.DV.find_element_by_class_name('pl-c__col').find_elements_by_class_name('pl-c__game')[0].click()
        sleep(5)
        #此处需要等待
        print('onClickToEarly End')

    # 具体比赛页面，寻找具体口水
    def findDetial(self, data):
        betType = data['bet_type_name']
        if betType in (17, 18):
            els = self.DV.find_elements_by_class_name('bettype')[0]  # 让球
            bettype_items = els.find_elements_by_class_name('bettype_item')
            for e in bettype_items:
                ds = e.text.replace('+', '').split('\n')  # '墨尔本胜利\n-0.25\n1.11\n0\n0.78\n+0.25\n0.58'
                name = ds[0]
                length = int((len(ds) - 1) / 2)
                for i in range(length):
                    pank = ds[i*2+1]
                    kof = ds[i*2+2]
                    if name == data['bet_name']:
                        if pank == str(data['market_and_bet_type_param']):
                            r = e.find_elements_by_class_name('bettype_oddsbox')[i]
                            return [r, kof]
        if betType == 19:  # 大
            els = self.DV.find_elements_by_class_name('bettype')[1]  # 让球
            bettype_items = els.find_elements_by_class_name('bettype_item')
            for e in bettype_items:
                ds = e.text.replace('+', '').split('\n')  # '墨尔本胜利\n-0.25\n1.11\n0\n0.78\n+0.25\n0.58'
                name = ds[0]
                length = int((len(ds) - 1) / 2)
                for i in range(length):
                    pank = ds[i * 2 + 1]
                    kof = ds[i * 2 + 2]
                    if name == '大':
                        if pank == str(data['market_and_bet_type_param']):
                            r = e.find_elements_by_class_name('bettype_oddsbox')[i]
                            return [r, kof]
        if betType == 20:
            els = self.DV.find_elements_by_class_name('bettype')[1]  # 让球
            bettype_items = els.find_elements_by_class_name('bettype_item')
            for e in bettype_items:
                ds = e.text.replace('+', '').split('\n')  # '墨尔本胜利\n-0.25\n1.11\n0\n0.78\n+0.25\n0.58'
                name = ds[0]
                length = int((len(ds) - 1) / 2)
                for i in range(length):
                    pank = ds[i * 2 + 1]
                    kof = ds[i * 2 + 2]
                    if name == '小':
                        if pank == str(data['market_and_bet_type_param']):
                            r = e.find_elements_by_class_name('bettype_oddsbox')[i]
                            return [r, kof]
        # 到这里 就说明未找到对应的口水
        print('未找到比赛对应的口水')
        print('数据网数据', data)
        return None

    def setcommatch_arrow(self):
        els_content = self.DV.find_elements_by_class_name('commatch_content')
        for e in els_content:
            if e.is_displayed():
                e.find_element_by_class_name('commatch_arrow').click()

    def findLeague(self, data_cell, bClick=True):
        xjwData = data_cell['xjw']
        hgwData = data_cell['hgw']
        # xjwData['started_at'] = self.updateTime(xjwData['started_at'])
        if self.isToDay(hgwData['started_at']):
            self.onClickToDay()
        else:
            self.onClickToEarly(hgwData['started_at'])
        self.setcommatch_arrow()
        els = self.DV.find_elements_by_class_name('commatch')
        for e in els:
            ary = e.text.split('\n')
            print(ary)
            time = ary[0]
            homeName = ary[1]
            awayName = ary[2]
            b1 = time == xjwData['started_at']
            b2 = homeName == xjwData['home']
            b3 = awayName == xjwData['away']
            if b2 and b3:
                e.find_element_by_class_name('commatch_header').find_element_by_class_name('commatch_home').location_once_scrolled_into_view
                sleep(2)
                e.find_element_by_class_name('commatch_header').find_element_by_class_name('commatch_home').click()
                sleep(2)
                e.find_element_by_class_name('commatch_content').find_element_by_class_name('commatch_home').click()
                sleep(2)
                WebDriverWait(self.DV, self._timeout).until(EC.presence_of_element_located((By.ID, "StreamingScoll")))
                print('找到比赛')
                return True
        print('未找到比赛')
        print(xjwData)
        return None

    def findLeagueToDetail(self, data):
        self.findLeague(data)
        es = self.findDetial(data['xjw'])
        return es


if __name__ == '__main__':
    xjwEngine = XjwRequest()
    xjwEngine.login()
