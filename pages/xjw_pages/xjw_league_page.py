from time import sleep

from pages.base_page import BasePage
from selenium.webdriver.common.by import By

from pages.xjw_pages.xjw_detail_page import XjwDetialPage

import numpy as np

class XjwLeaguesPage(BasePage):
    """
    比赛列表页面
    """

    def arrows(self):
        ary = []
        arr = self.find_emelemts(By.CLASS_NAME, 'commatch_content')
        for e in arr:
            if e.is_displayed():
                v = e.find_element_by_class_name('commatch_arrow')
                ary.append(v)
        return ary

    def leagues(self):
        return self.find_emelemts(By.ID, 'commatch')

    def getLeaguesData(self):
        elves = self.leagues()
        retData = []
        for e in elves:
            ary = e.text.split('\n')
            if len(ary) >= 3:
                time = ary[0]
                homeName = ary[1]
                awayName = ary[2]
                retData.append({
                    e,
                    time,
                    homeName,
                    awayName
                })
        return retData

    def goLeague(self,hName, aName):
        leagues = self.getLeaguesData()
        for item in leagues:
            b1 = item['homeName'] == hName
            b2 = item['awayName'] == aName
            if b1 and b2:
                e = item['e']
                e.find_element_by_class_name('commatch_header').find_element_by_class_name('commatch_home').location_once_scrolled_into_view  # 定位到
                sleep(1)
                e.find_element_by_class_name('commatch_header').find_element_by_class_name('commatch_home').click()
                sleep(2)  # 上面点击展开比赛后，这边可能存在网络不好卡住 Wait
                e.find_element_by_class_name('commatch_content').find_element_by_class_name('commatch_home').click()
                return XjwDetialPage(self.driver)

    def saveData(self):
        """
        字典格式  时间
        :return:
        """
        rets = np.loadtxt("data.npy", allow_pickle=True)

        datas = self.getLeaguesData()
        length = len(datas)
        for i in range(length):
            d = datas[i]
            time = d['time'].split(' ')[1]
            v = d['homeName'] + '/' + d['awayName']
            if time not in rets.keys():
                rets[time] = {}
                rets[time]['xjw'] = []
            if v not in rets[time]['xjw']:
                rets[time]['xjw'].append(v)

        np.savetxt('data.txt', rets)
        return rets



    def onAdjustArrow(self):
        arrows = self.arrows()
        for e in arrows:
                e.click()



