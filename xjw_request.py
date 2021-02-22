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
        self._timeout = 30
        self._usr = 'siegjan'
        self._pwd = 'Zhouj5134'
        mobileEmulation = {'deviceName': 'iPhone X'}
        self.OPTIONS = webdriver.ChromeOptions()
        self.OPTIONS.add_argument('--ignore-certificate-errors')
        self.OPTIONS.add_experimental_option('mobileEmulation', mobileEmulation)
        self.DV = webdriver.Chrome(executable_path='chromedriver.exe', options=self.OPTIONS)
        self._linkIndex = 0
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
            if self.webDriverWat(By.CLASS_NAME,'no-acc-path') is None:
                return self.openLoginPage()

        except:
            print('找不到登录页面的元素，或者网站登录页面打开超时', self._linkIndex)
            self._linkIndex = self._linkIndex + 1
            return self.openLoginPage()
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
        sleep(4)
        self.DV.find_element_by_id('gologin').click()
        sleep(5)
        # 这里出现验证码 class
        try:
            WebDriverWait(self.DV, self._timeout).until(EC.presence_of_element_located((By.CLASS_NAME, "popup-wrap")))
            sleep(6)  # 这秒内完成验证码验证
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
        """
        打开 进入亚洲体育
        :return: None or True
        """
        if self.webDriverWat(By.ID, 'gamelist') is None:
            return None
        try:
            continue_link = self.DV.find_element_by_link_text('亚洲体育')
            continue_link.click()
            sleep(3)
            # 弹出新页面 ,进入新页面（亚洲体育）

            sleep(5)
            e = self.webDriverWat(By.CLASS_NAME, 'btn-reset')
            # e = self.DV.find_element_by_class_name('btn-reset')
            if e is None:
                return None
            e.click()
            print('openYazhou End')
            self._baseURL = self.DV.current_url
            return True
        except:
            self._baseURL = self.DV.current_url
            print('异常 openYazhou')
            return None
        else:
            return True


    # 打开网址到登录完毕
    def login(self):
        b = self.openLoginPage()
        if not b:
            return b
        self._clicknoaccpath()
        self.pushUsrPwd()
        if self.openYazhou() is None:
            return None
        print('初始化完毕')
        return True

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

    def onClickToDay(self, isNow=True):  # 今日
        """
        点击 今日 ， 足球
        :param isNow: True,False (今日，早盘）
        :return: True or None
        """
        e = self.webDriverWat(By.CLASS_NAME, 'pl-c__menu', False)
        # if e is None:
        #     if self.goHome() is None:
        #         return None

        try:
            if isNow:
                e.find_elements_by_class_name('pl-c__btn')[0].click()
            else:
                e.find_elements_by_class_name('pl-c__btn')[1].click()
            sleep(0.5)

            sleep(3)
        except:
            print('异常 onClickToDay')
            return None
        else:
            return True

    # 具体比赛页面，寻找具体口水
    def findDetial(self, data):
        WebDriverWait(self.DV, self._timeout).until(
            EC.presence_of_element_located((By.ID, "StreamingScoll")))
        betType = data['bet_type_name']
        if betType in (17, 18):
            els = self.DV.find_elements_by_class_name('bettype')[0]  # 让球
            bettype_items = els.find_elements_by_class_name('bettype_item')
            for e in bettype_items:
                ds = e.text.replace('+', '').split('\n')  # '墨尔本胜利\n-0.25\n1.11\n0\n0.78\n+0.25\n0.58'
                name = ds[0]
                length = int((len(ds) - 1) / 2)
                for i in range(length):
                    pank = ds[i * 2 + 1]
                    kof = ds[i * 2 + 2]
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

    def webDriverWat(self, b, v,isRefash=True):
        """
        等待页面
        :param b: By.ID ,By.CLASS_NAME
        :param v:  btn-login
        :return:  element or None
        """
        try:
            e = WebDriverWait(self.DV, self._timeout).until(EC.presence_of_element_located((b, v)))
        except:
            print('等待异常 webDriverWat', b, v, self._linkIndex)
            if self._linkIndex >=5 or isRefash is False:
                self._linkIndex = 0
                return None
            self._linkIndex = self._linkIndex + 1
            self.DV.refresh()
            return self.webDriverWat(b, v)
        else:
            self._linkIndex = 0
            return e

    def setcommatch_arrow(self):
        """
        关闭默认展开的前三个比赛
        :return:  None or True
        """
        r = self.webDriverWat(By.CLASS_NAME, 'commatch_content')  # 等待早盘或者今日比赛列表页面
        if r is None:
            return None
        try:
            els_content = self.DV.find_elements_by_class_name('commatch_content')
            for e in els_content:
                if e.is_displayed():
                    e.find_element_by_class_name('commatch_arrow').click()
                    sleep(1)
        except:
            print('异常 setcommatch_arrow ')
            return None
        else:
            return True

    def findDayPageEx(self):
        """
        调用 今日和早盘的 比赛 数据
        :return: {} 返回数据格式 时间 - 网站 - 比赛（数组）
        """
        r1 = self.findDayPage(True)
        print(r1)
        r2 = self.findDayPage(False)
        r1.update(r2)
        return r1

    def goHome(self):
        print('goHome ', self._baseURL)
        self.DV.get(self._baseURL)
        if self.webDriverWat(By.CLASS_NAME, 'pl-c__menu') is None:
            return None
        return True

    def findDayPage(self, isNow=True):
        """
        查找今日和早盘比赛的队伍数据，用来映射队伍名称使用
        :param started_at: 时间戳
        :return: {} 返回数据格式 时间 - 网站 - 比赛（数组）
        """
        if self.onClickToDay(isNow) is None:
            return None

        if self.setcommatch_arrow() is None:
            return None
        # try:
        elves = self.DV.find_elements_by_class_name('commatch')  # 所有的比赛节点
        retData = {}
        for e in elves:
            ary = e.text.split('\n')
            print(ary)
            if len(ary) >= 3:
                time = ary[0].split(' ')[1]
                homeName = ary[1]
                awayName = ary[2]
                v = homeName + '/' + awayName
                if time not in retData.keys():
                    retData[time] = {}
                    retData[time]['xjw'] = []
                if v not in retData[time]['xjw']:
                    retData[time]['xjw'].append(homeName + '/' + awayName)
                print(retData[time]['xjw'])
        # except:
        #     print('异常 findDayPage', isNow)
        #     assert AssertionError
        #     return {}
        # else:
        return retData


    def findLeague(self, p_home,p_away, p_started_at):
        """
        在比赛页面中 查找需要的比赛
        :param p_home: 队伍A
        :param p_away: 队伍B
        :param p_started_at: 比赛时间
        :return: None or True
        """
        # 此处缺一个等待 之前如果是arrow就没问题
        try:
            els = self.DV.find_elements_by_class_name('commatch')  # 所有的比赛节点
            for e in els:
                ary = e.text.split('\n')
                print(ary)
                time = ary[0]
                homeName = ary[1]
                awayName = ary[2]
                b2 = homeName == p_home
                b3 = awayName == p_away
                if b2 and b3:  # 查找比赛没有按比赛时间查找
                    e.find_element_by_class_name('commatch_header').find_element_by_class_name(
                        'commatch_home').location_once_scrolled_into_view  # 定位到
                    sleep(1)
                    e.find_element_by_class_name('commatch_header').find_element_by_class_name('commatch_home').click()
                    sleep(2)  # 上面点击展开比赛后，这边可能存在网络不好卡住 Wait
                    e.find_element_by_class_name('commatch_content').find_element_by_class_name('commatch_home').click()
                    sleep(1)
                    return True
        except:
            print('异常')
            return None
        else:
            print('未找到比赛', p_home, p_away, p_started_at)
            return None

    def findLeagueToDetail(self, data):
        h = data['hgw']['home']
        a = data['hgw']['away']
        s = data['hgw']['started_at']
        if self.findLeague(h, a, s) is None:
            return None
        es = self.findDetial(data['xjw'])
        return es



if __name__ == '__main__':
    xjwEngine = XjwRequest()
    xjwEngine.login()
    data = xjwEngine.findDayPageEx()
    print(data)
