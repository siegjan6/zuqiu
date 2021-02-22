# encoding: utf-8
# !/usr/bin/env python
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC  # available since 2.26.0

from selenium import webdriver
from selenium.webdriver.common.by import By

DEFAULT_SECOND = 20


class BasePage:
    def __init__(self, dr, url=None):
        self.driver = dr
        if not None:
            self.base_url = url

    def _open(self, url):
        self.driver.get(url)

    def open(self):
        self._open(self.base_url)

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
            # 保证元素可见
            print('findEments', by, value)
            WebDriverWait(self.driver, DEFAULT_SECOND).until(EC.visibility_of_all_elements_located(by, value))
            return self.driver.find_elements(by,value)
        except:
            print("页面中没有 %", by, value)
        return None

    def switch_to_window(self, i):
        hands = self.driver.window_handles;
        if len(hands) > i:
            self.driver.switch_to_window(self.driver.window_handles[i])
        else:
            print('异常 switch_to_window index:', i)
