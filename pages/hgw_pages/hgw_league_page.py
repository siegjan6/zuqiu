from datetime import timedelta
from time import sleep

from selenium.webdriver.common.keys import Keys

from pages.base_page import BasePage
from selenium.webdriver.common.by import By

import configparser
import datetime
from pages.hgw_pages.hgw_detail_page import HgwDetialPage


class HgwLeaguesPage(BasePage):
    """
    比赛列表页面
    """
    _path = 'C:/Users/Administrator/Documents/GitHub/zuqiu/tmp/config.ini'

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
        leagues = self.getLeaguesData()
        for item in leagues:
            b1 = item['homeName'] == hName
            b2 = item['awayName'] == aName
            if b1 and b2:
                e = item['e']
                e.location_once_scrolled_into_view
                e.click()
                return HgwDetialPage(self.driver)

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
        datas = self.getLeaguesData()
        length = len(datas)
        for i in range(length):
            d = datas[i]
            time = d['time'].split(' ')[-1]
            hour = time.split(':')[0]
            if hour == '24':
                hour = '0'
            min = '0'
            if len(time.split(':')) > 1:
                min = time.split(':')[1]
            dt = datetime.datetime(2021, 2, 23, int(hour), int(min), 0)

            interval = timedelta(hours=12)
            dt = dt + interval
            time = dt.strftime('%H:%M')

            v = 'hgw/' + d['homeName'] + '/' + d['awayName']
            if time not in config:
                config.add_section(time)

            if v not in config[time]:
                config.set(time, v, '1')
                
        config.write(open(self._path, 'w'))
