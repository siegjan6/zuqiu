# encoding: utf-8
# !/usr/bin/env python
from time import sleep

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC  # available since 2.26.0

from selenium import webdriver
from selenium.webdriver.common.by import By

DEFAULT_SECOND = 15


class BasePage:
    def __init__(self, dr, url=None):
        self.driver = dr
        if url :
            self.base_url = url

    def _open(self, url):
        self.driver.get(url)

    def open(self):
        """
        打开网页
        :return:
        """
        try:
            if self.driver.current_url != self.base_url:
                self._open(self.base_url)
            return True
        except:
            print('open field')
            return False


    def find_emelemt(self, by, value):
        try:
            # 保证元素可见
            print('findEment', by, value)
            WebDriverWait(self.driver, DEFAULT_SECOND).until(EC.visibility_of_all_elements_located((by, value)))
            return self.driver.find_element(by, value)
        except:
            print("页面中没有 %", by, value)
        return None

    def find_emelemts(self, by, value):
        try:
            print('findEments', by, value)
            WebDriverWait(self.driver, DEFAULT_SECOND).until(EC.visibility_of_element_located((by, value)))
            sleep(3)
            return self.driver.find_elements(by, value)
        except:
            print("页面中没有 或等待超时", by, value)
        return None

    def switch_to_window(self, i):
        hands = self.driver.window_handles;
        if len(hands) > i:
            self.driver.switch_to_window(self.driver.window_handles[i])
        else:
            print('异常 switch_to_window index:', i)

    def close(self):
        self.driver.close()

    def click(self, e):
        self.driver.execute_script("arguments[0].click();", e)
        sleep(1)

    def is_alert(self):
        result = EC.alert_is_present()(self.driver)
        if result:
            print(result.text)
            result.accept()
            return True
        else:
            print("alert未弹出")
            return False

    def wait_all(self, by, v):
        print('wait_all', by, v)
        return WebDriverWait(self.driver, 60).until(EC.presence_of_all_elements_located((by, v)))

    def wait_txt(self, by, v, txt):
        r = WebDriverWait(self.driver, 60).until(EC.text_to_be_present_in_element((by, v), txt))
        return r

    def invisibility_of_element_located(self, by, v):
        print('invisibility_of_element_located', by, v)
        return WebDriverWait(self.driver, 60).until(EC.invisibility_of_element_located((by, v)))

    def find_elements_by_css(self, css_selector):
        # css_selector = 'input[id*=body_R_FT_]'
        return self.driver.find_elements_by_css_selector(css_selector)
# def findElement(driver,element,by,value):
#     try:
#         # 保证元素可见
#         print('findElement', by, value)
#         WebDriverWait(self.driver, DEFAULT_SECOND).until(EC.visibility_of_all_elements_located((by, value)))
#         return self.driver.find_element(by, value)
#     except:
#         print("页面中没有 %", by, value)
#     return None