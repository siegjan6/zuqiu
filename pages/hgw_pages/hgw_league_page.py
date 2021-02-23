from time import sleep

from selenium.webdriver.common.keys import Keys

from pages.base_page import BasePage
from selenium.webdriver.common.by import By


import numpy as np
import configparser

from pages.hgw_pages.hgw_detail_page import HgwDetialPage


class HgwLeaguesPage(BasePage):
    """
    比赛列表页面
    """
    _path = 'tmp/config.ini'

    def tab_main(self):  # 主要玩法 按钮
        return self.find_emelemt(By.ID, 'tab_main')

    def html(self):  # 用来按键盘核对焦点
        return self.DV.find_element_by_tag_name('html')

    def box_lebet_l(self): ## 比赛
        return self.find_emelemt(By.CLASS_NAME, 'box_lebet_l')

    def getLeaguesData(self):
        self.tab_main().click()
        html = self.html()
        retData = []
        _leagues = {}
        l = -1
        while len(_leagues) != l:
            l = len(_leagues)
            temams = self.btn_inn_teams()
            length = len(temams)
            for i in range(length):
                try:
                    e = temams[i]
                    print(e)
                    ary = e.text.split('\n')
                    if len(ary) < 3:
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
        leagues = self.getLeaguesData()
        for item in leagues:
            b1 = item['homeName'] == hName
            b2 = item['awayName'] == aName
            if b1 and b2:
                e = item['e']
                e.location_once_scrolled_into_view
                e.click()
                return HgwDetialPage(self.driver)

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
            time = d['time'].split(' ')[1]
            v = 'xjw/' + d['homeName'] + '/' + d['awayName']
            if time not in config:
                config.add_section(time)

            if v not in config[time]:
                config.set(time, v, '1')

        config.write(open(self._path, 'w'))



