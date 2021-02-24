import datetime
import time

from pages.base_page import BasePage
from selenium.webdriver.common.by import By

from pages.hgw_pages.hgw_league_page import HgwLeaguesPage


def isToDay(day):
    now = datetime.datetime.now()
    d1 = now.day
    d2 = day
    return d1 == d2


class HgwHomePage(BasePage):
    """
    游戏页
    """

    # def __init__(self):
    #     super(BasePage, self).__init__()
    #     self.url = self.driver.current_url

    def today_page(self):  # 今日
        return self.find_emelemt(By.ID, 'today_page')

    def early_page(self):  # 早盘
        return self.find_emelemt(By.ID, 'early_page')

    def btn_coupon1(self):  # 比赛行
        self.invisibility_of_element_located(By.ID, 'loading')
        self.invisibility_of_element_located(By.CLASS_NAME, 'loading')
        s = self.find_emelemt(By.ID, 'btn_coupon1')
        return s

    def date_icon(self):  # 出现日期按钮
        self.invisibility_of_element_located(By.ID, 'loading')
        self.invisibility_of_element_located(By.CLASS_NAME, 'loading')
        s = self.find_emelemt(By.ID, 'date_icon')
        time.sleep(1)
        return s

    def btn_dates(self):  # 出现日期按钮 数组
        return self.find_emelemts(By.CLASS_NAME, 'btn_date')

    def symbol_ft(self):
        self.invisibility_of_element_located(By.ID, 'loading')
        self.invisibility_of_element_located(By.CLASS_NAME, 'loading')
        return self.find_emelemt(By.ID, 'symbol_ft')

    def _goDay(self, day):
        if isToDay(day):
            self.today_page().click()
            ft_btn = self.symbol_ft()
            if not ft_btn:
                return False
            self.btn_coupon1().click()
            return True
        else:
            self.early_page().click()
            self.symbol_ft().click()
            self.date_icon().click()
            elements = self.btn_dates()
            for e in elements:
                ary = e.text.split('\n')
                if len(ary) == 3 and ary[1] == str(day):
                    e.click()
                    self.btn_coupon1().click()
                    return True
        print('goDay error', day)
        return False

    def goDay(self, day):
        try:
            self._goDay(day)
            return HgwLeaguesPage(self.driver)
        except:
            print('goDay field')
            return False
