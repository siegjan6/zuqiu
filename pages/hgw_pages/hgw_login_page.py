from time import sleep

from pages.base_page import BasePage
from selenium.webdriver.common.by import By

from pages.hgw_pages.hgw_home_page import HgwHomePage

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
        try:
            self.username().send_keys(u)
            self.password().send_keys(p)
            self.wait_all(By.CLASS_NAME, 'btn_login')
            self.click(self.login_btn())
            self.no_btn().click()
            return HgwHomePage(self.driver)
        except:
            print('login field')
            return False

