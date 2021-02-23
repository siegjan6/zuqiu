from pages.base_page import BasePage
from selenium.webdriver.common.by import By

from pages.hgw_pages.hgw_home_page import HgwHomePage


class HgwLoginPage(BasePage):
    """
    登录页
    """

    def username(self):
        return self.find_emelemt(By.ID, 'usr')

    def password(self):
        return self.find_emelemt(By.ID, 'pwd')

    def login_btn(self):
        return self.find_emelemt(By.ID, 'btn_login')

    def no_btn(self):
        return self.find_emelemt(By.ID, 'no_btn')

    def logIn(self, u, p):
        self.username().send_keys(u)
        self.password().send_keys(p)
        self.login_btn().click()
        self.no_btn().click()
        return HgwHomePage(self.driver)
