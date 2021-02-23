from pages.base_page import BasePage
from selenium.webdriver.common.by import By

from pages.xjw_pages.xjw_league_page import XjwLeaguesPage


class XjwHomePage(BasePage):
    """
    游戏页
    """

    def _menus(self):
        return self.find_emelemt(By.CLASS_NAME, 'pl-c__menu')

    def _games(self):
        return self.driver.find_element_by_class_name('pl-c__col')

    def day(self):
        menus = self._menus()
        bbtns = self.find_emelemts(By.CLASS_NAME, 'pl-c__btn')
        return bbtns[0]

    def elary(self):
        menus = self._menus()
        bbtns = self.find_emelemts(By.CLASS_NAME, 'pl-c__btn')
        return bbtns[1]

    def fb(self):
        g = self._games()
        return g.find_elements_by_class_name('pl-c__game')[0]

    def goDay(self, isToDay):
        if isToDay:
            self.day().click()
        else:
            self.elary().click()
        self.fb().click()
        return XjwLeaguesPage(self.driver)