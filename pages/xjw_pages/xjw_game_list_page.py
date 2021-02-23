from pages.base_page import BasePage
from selenium.webdriver.common.by import By

from pages.xjw_pages.xjw_home_page import XjwHomePage


class XjwGameListPage(BasePage):
    """
    游戏列表页（登录后）
    """

    def yazhou(self):
        return self.find_emelemt(By.LINK_TEXT, '亚洲体育')

    def reset_btn(self):  # 忽略按钮
        return self.find_emelemt(By.CLASS_NAME, 'btn-reset')

    def goNextPage(self):
        self.yazhou().click()
        self.switch_to_window(1)
        try:
            self.reset_btn().click()
        except:
            print('err reset_btn().click()')
        return XjwHomePage(self.driver)
