from time import sleep

from pages.base_page import BasePage
from selenium.webdriver.common.by import By

from pages.xjw_pages.xjw_detail_page import XjwDetialPage


import configparser


class XjwLeaguesPage(BasePage):
    """
    比赛列表页面
    """
    _path = 'tmp/config.ini'

    def arrows(self):
        ary = []
        arr = self.find_emelemts(By.CLASS_NAME, 'commatch_content')
        for e in arr:
            if e.is_displayed():
                v = e.find_element_by_class_name('commatch_arrow')
                if v.is_displayed():
                    ary.append(v)
        return ary

    def leagues(self):
        return self.find_emelemts(By.CLASS_NAME, 'commatch')

    def getLeaguesData(self):
        self.onAdjustArrow()
        elves = self.leagues()
        retData = []
        for e in elves:
            ary = e.text.split('\n')
            if len(ary) >= 3:
                time = ary[0]
                homeName = ary[1]
                awayName = ary[2]
                retData.append({
                    'e': e,
                    'time': time,
                    'homeName': homeName,
                    'awayName': awayName
                })
        return retData

    def goLeague(self, hName, aName):
        leagues = self.getLeaguesData()
        for item in leagues:
            b1 = item['homeName'] == hName
            b2 = item['awayName'] == aName
            if b1 and b2:
                e = item['e']
                e.find_element_by_class_name('commatch_header').find_element_by_class_name('slideshow_1').location_once_scrolled_into_view  # 定位到
                sleep(1)
                self.click(e.find_element_by_class_name('commatch_header').find_element_by_class_name('slideshow_1'))
                sleep(5)  # 上面点击展开比赛后，这边可能存在网络不好卡住 Wait
                self.click(e.find_element_by_class_name('commatch_content').find_element_by_class_name('commatch_home'))
                print('innerXjwDetialPage')
                return XjwDetialPage(self.driver)

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


    def onAdjustArrow(self):
        arrows = self.arrows()
        try:
            for e in arrows:
                self.click(e)
                sleep(0.5)
        except:
            print('onAdjustArrow error', e)



