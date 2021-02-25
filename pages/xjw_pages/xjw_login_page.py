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

    def login(self, u, p):
        self.username().send_keys(u)
        self.password().send_keys(p)
        self.login_btn().click()
        temp = input('完成验证码后，按任意键继续')
        self.invisibility_of_element_located(By.ID, 'dx_captcha_basic_pic_1')
        self.xjwGanmeList = XjwGameListPage(self.driver)
        page = self.xjwGanmeList.goNextPage()
        return page

    def goHome(self):
        hands = self.driver.window_handles
        if len(hands) > 1:
            self.close()
            self.switch_to_window(0)
            return self.xjwGanmeList.goNextPage()
        else:
            print('异常 switch_to_window goHome:')