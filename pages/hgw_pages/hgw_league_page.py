from datetime import timedelta
from time import sleep

from selenium.webdriver.common.keys import Keys

from pages.base_page import BasePage
from selenium.webdriver.common.by import By

import configparser
import datetime
from pages.hgw_pages.hgw_detail_page import HgwDetialPage

import getpass

class HgwLeaguesPage(BasePage):
    """
    比赛列表页面
    """
    _path = 'C:/Users/'+getpass.getuser()+'/Documents/GitHub/zuqiu/tmp/temp.ini'
    _item_config_path = 'C:/Users/'+getpass.getuser()+'/Documents/GitHub/zuqiu/tmp/item_config.ini'
    _posDatas = {

    }  # dayNUm:v

    def tab_main(self):  # 主要玩法 按钮
        return self.find_emelemt(By.ID, 'tab_main')

    def html(self):  # 用来按键盘核对焦点
        return self.driver.find_element_by_tag_name('html')

    def box_lebet_l(self): ## 比赛
        return self.find_emelemts(By.CLASS_NAME, 'box_lebet_l')

    def getLeaguesData(self):
        self.invisibility_of_element_located(By.ID, 'loading')
        self.invisibility_of_element_located(By.CLASS_NAME, 'loading')
        html = self.html()
        self.tab_main().click()
        self.invisibility_of_element_located(By.ID, 'loading')
        self.invisibility_of_element_located(By.CLASS_NAME, 'loading')
        retData = []
        _leagues = {}
        l = -1
        while len(_leagues) != l:
            l = len(_leagues)
            temams = self.box_lebet_l()
            length = len(temams)
            for i in range(length):
                try:
                    e = temams[i]
                    print(e.text)
                    if not e:
                        continue
                    if not e.text:
                        continue
                    ary = e.text.split('\n')
                    if len(ary) < 3:
                        continue
                    if ary[1] in _leagues.keys():
                        continue

                    time = ary[0]
                    homeName = ary[1]
                    awayName = ary[2]
                    retData.append({
                        'e': e,
                        'time': time,
                        'homeName': homeName,
                        'awayName': awayName
                    })


                    _leagues[ary[1]] = ary[2]

                except ValueError:
                    continue
            html.send_keys(Keys.ARROW_DOWN * 40)
        return retData

    def goLeague(self, hName, aName):
        """
        有问题
        :param hName:
        :param aName:
        :return:
        """
        self.invisibility_of_element_located(By.ID, 'loading')
        self.invisibility_of_element_located(By.CLASS_NAME, 'loading')
        html = self.html()
        self.tab_main().click()
        self.invisibility_of_element_located(By.ID, 'loading')
        self.invisibility_of_element_located(By.CLASS_NAME, 'loading')
        retData = []
        _leagues = {}
        l = -1
        while len(_leagues) != l:
            l = len(_leagues)
            temams = self.box_lebet_l()
            length = len(temams)
            for i in range(length):
                try:
                    e = temams[i]
                    print(e.text)
                    if not e:
                        continue
                    if not e.text:
                        continue
                    ary = e.text.split('\n')
                    if len(ary) < 3:
                        continue
                    if ary[1] in _leagues.keys():
                        continue

                    time = ary[0]
                    homeName = ary[1]
                    awayName = ary[2]
                    retData.append({
                        'e': e,
                        'time': time,
                        'homeName': homeName,
                        'awayName': awayName
                    })
                    b1 = homeName == hName
                    b2 = awayName == aName
                    if b1 and b2:
                        # e.location_once_scrolled_into_view
                        e.click()
                        # self.invisibility_of_element_located(By.ID, 'loading')
                        # self.invisibility_of_element_located(By.CLASS_NAME, 'loading')
                        return HgwDetialPage(self.driver)
                    _leagues[ary[1]] = ary[2]
                except ValueError:
                    continue
            html.send_keys(Keys.ARROW_DOWN * 40)
        return False

    def updateTime(self, t):
        interval = timedelta(hours=12)
        d = datetime.datetime.fromtimestamp(t)
        d = d + interval
        return d.timestamp()

    def saveData(self):
        """
        字典格式  时间
        :return:
        """
        config = configparser.ConfigParser()
        config.read(self._path)

        item_config = configparser.ConfigParser()
        item_config.read(self._item_config_path)

        datas = self.getLeaguesData()
        length = len(datas)
        for i in range(length):
            d = datas[i]
            timeary = d['time'].split(' ')
            time = timeary[-1]
            hour = time.split(':')[0]
            if hour == '24':
                hour = '0'
            min = '0'
            month=''
            day = ''
            dt = ''
            temp =timeary[0]
            if temp == '今日':
                day = datetime.datetime.now().today()
                month = datetime.datetime.now().month()
            elif '星期' in temp:
                month = timeary[3]
                day = timeary[1]

            if len(time.split(':')) > 1:
                min = time.split(':')[1]
            try:
                dt = datetime.datetime(2021, int(month), int(day), int(hour), int(min), 0)
            except:
                continue

            interval = timedelta(hours=12)
            dt = dt + interval
            time = dt.strftime('%m-%d-%H:%M')

            v = 'hgw/' + d['homeName'] + '/' + d['awayName']
            if time not in config:
                config.add_section(time)

            if v not in config[time]:
                if d['homeName'] not in item_config['name']:
                    continue
                if d['awayName'] not in item_config['name']:
                    continue
                config.set(time, v, '2')
                
        config.write(open(self._path, 'w'))
