# from selenium import webdriver
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC  # available since 2.26.0

from selenium.webdriver.common.keys import Keys
from time import sleep

from browsermobproxy import Server
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

#
mobileEmulation = {'deviceName': 'iPhone 6/7/8 Plus'}
OPTIONS = webdriver.ChromeOptions()
OPTIONS.add_argument('--ignore-certificate-errors')
OPTIONS.add_experimental_option('mobileEmulation', mobileEmulation)
DV = webdriver.Chrome(executable_path='chromedriver.exe', options=OPTIONS)
DV.get('http:/11mx.cc')
DV.find_element_by_class_name('no-acc-path').click()  # 已有账号，登录

DV.find_element_by_id('uid').send_keys('siegjan')
DV.find_element_by_id('jpwd').send_keys('Zhouj5134')
DV.find_element_by_id('gologin').click()
##这里需要验证码
continue_link = DV.find_element_by_link_text('亚洲体育')
# 弹出新页面
DV.switch_to_window(DV.window_handles[1])

DV.find_element_by_link_text('忽略提醒进入游戏').click()
# 漫长等待  长时间没反应可以尝试刷新 DV.refresh()
# 在这里判断 早盘还是今日
# __________________________________________________________________________________
DV.find_elements_by_class_name('commatch_content')  # 有点多，需要过滤掉为空的text


def temp(e):
    return e.text != ''

# 关闭
els_content = DV.find_elements_by_class_name('commatch_content')
for e in els_content:
    if e.is_displayed():
        e.find_element_by_class_name('commatch_arrow').click()

DV.find_elements_by_class_name('commatch_content')[2].find_element_by_class_name('commatch_arrow').click()


els = DV.find_elements_by_class_name('commatch_content')
print(len( DV.find_elements_by_class_name('commatch_content')))
els = list(filter(temp, els))
print(len(els))
for e in els:
    print(e.text)

len(DV.find_elements_by_class_name('commatch_header'))
DV.find_element_by_class_name('btn-reset')

# gologin
DV.find_element_by_id('no_btn').click()
DV.find_element_by_class_name('no_acc-path').click()
server = Server('.\\browsermob-proxy-master\\browsermob-dist\src\main\scripts\\browsermob-proxy.bat')

server.start()
proxy = server.create_proxy()

del DV.requests
# 拦截https://github.com/wkeeling/selenium-wire#intercepting-requests-and-responses
for request in DV.requests:
    if request.path == '/transform.php':
        if request.response:
            ll = int(request.response.headers['Content-Length'])
            if ll > 2000:
                print(ll)

dd = DV.find_element_by_class_name('title_event')
dd.click()
request = DV.wait_for_request('/transform.php$')
print(request)


# self.DV.find_element_by_class_name('menu-market').click()   # 点击菜单选择时间
# self.DV.find_element_by_link_text('今日').click()
# self.DV.find_element_by_link_text('早盘').click()
# self.DV.find_element_by_class_name('search-input').click()  # 搜索
# self.DV.find_element_by_id('InputSearch').send_keys('澳洲') #搜索输入
# e = WebDriverWait(self.DV, self._timeout).until(EC.presence_of_element_located((By.CLASS_NAME, "dropdown-menu")))
# self.DV.find_element_by_link_text('澳洲甲组联赛').click() #点击搜索结果
# self.DV.find_element_by_class_name('icon-arrow-right').click()   # 第一个进去

## self.DV.find_elements_by_class_name('commatch_header') 所有的比赛

# 会未找到比赛，