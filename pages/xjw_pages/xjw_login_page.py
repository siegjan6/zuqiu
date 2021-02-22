from pages.base_page import BasePage
from selenium.webdriver.common.by import By

from pages.xjw_pages.xjw_game_list_page import XjwGameListPage


class XjwLoginPage(BasePage):
    """
    登录页
    """

    def username(self):
        return self.find_emelemt(By.ID, 'uid')

    def password(self):
        return self.find_emelemt(By.ID, 'jpwd')

    def login_btn(self):
        return self.find_emelemt(By.ID, 'gologin')

    def logIn(self, u, p):
        self.username().send_keys(u)
        self.password().send_keys(p)
        self.login_btn().click()
        temp = input('等待验证码通过 y or n')
        return XjwGameListPage(self.driver)
