from pages.base_page import BasePage
from selenium.webdriver.common.by import By

from pages.xjw_pages.xjw_home_page import XjwHomePage
import time
import re
class XjwGameListPage(BasePage):
    """
    游戏列表页（登录后）
    """

    def yazhou(self):
        return self.find_emelemt(By.LINK_TEXT, '亚洲体育')

    def reset_btn(self):  # 忽略按钮
        time.sleep(3)
        self.invisibility_of_element_located(By.CLASS_NAME, 'preloader_spiner')
        return self.driver.find_element_by_class_name('btn-reset')
        # return self.driver.find_(By.CLASS_NAME, 'btn-reset')

    def goNextPage(self):
        self.yazhou().click()
        self.switch_to_window(1)

        self.invisibility_of_element_located(By.CLASS_NAME, 'preloader_spiner')
        txt = self.find_emelemt(By.CLASS_NAME, 'blockPage').text
        print(txt)
        if txt:
            t = re.findall(r'[(](.*?)[)]', self.find_emelemt(By.CLASS_NAME, 'blockPage').text)[0]
            return False

        self.click(self.reset_btn())
        self.invisibility_of_element_located(By.CLASS_NAME, 'preloader_spiner')

        return XjwHomePage(self.driver)
