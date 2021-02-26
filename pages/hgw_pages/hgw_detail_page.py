from pages.base_page import BasePage
from selenium.webdriver.common.by import By
import time
def isAllZh(s):
    """
    包含汉字的返回TRUE
    :param s:
    :return:
    """
    for c in s:
        if '\u4e00' <= c <= '\u9fa5':
            return True
    return False

def getParam(txt):
    txts = txt.split('\n')
    if isAllZh(txts[3]):
        return txts[1]
    return txts[3]

class HgwDetialPage(BasePage):

    def _findLeague(self, betType, betName, betParam):
        self.invisibility_of_element_located(By.ID, 'loading')
        self.invisibility_of_element_located(By.CLASS_NAME, 'loading')
        """

        :param betType: 17,18,19,20
        :param betName: 要打的队名，
        :param betParam: 盘口 1.25
        :return:
        """
        betParam = abs(float(betParam))
        if betType in (17, 18):  # 找球队名称 17是+的，18是-的，数据网没有+号 为0就没有正负号
            eves = self.body_R_FT_S()
            for e in eves:
                _eles = e.find_elements_by_class_name('btn_lebet_odd')
                param = getParam(e.text)  # pank
                if '/' in param:
                    a = param.split('/')
                    param = float((float(a[0]) + float(a[1]))/2)
                else:
                    param = float(param)

                if betParam == param:
                    for v in _eles:
                        txts = v.text.split('\n')
                        name = txts[0]
                        kof = txts[-1]
                        if betName == name:
                            return [kof, v]
        elif betType in (19, 20):
            if betType == 19: betName = '大'
            if betType == 20: betName = '小'
            self.body_OU_FT_S()[0].location_once_scrolled_into_view
            eves = self.body_OU_FT_S()
            for e in eves:
                _eles = e.find_elements_by_class_name('btn_lebet_odd')
                param = e.text.split('\n')[1]  # pank
                if '/' in param:
                    a = param.split('/')
                    param = float((float(a[0]) + float(a[1])) / 2)
                else:
                    param = float(param)

                if betParam == param:
                    for v in _eles:
                        txts = v.text.split('\n')
                        name = txts[0]
                        kof = txts[-1]
                        if betName == name:
                            return [kof, v]
        print('没有找到盘口', param, betName)
        return False
#self.find_elements_by_css( 'div[id*=body_R_FT_]')[0].find_elements_by_class_name('btn_lebet_odd')[0].text

    def findLeagueKof(self, betType, betName, betParam):
        ary = self._findLeague(betType, betName, betParam)
        if ary:
            return ary[0]
        return False

    def findLeagueDOM(self, betType, betName, betParam):
        ary = self._findLeague(betType, betName, betParam)
        if ary:
            return ary[1]
        return False

    def body_R_FT_S(self):  # 让球
        css_selector = 'div[id*=body_R_FT_]'
        return self.find_elements_by_css( 'div[id*=body_R_FT_]')

    def body_OU_FT_S(self):  # 大小
        css_selector = 'div[id*=body_OU_FT_]>div[id*=bet_]'
        return self.find_elements_by_css(css_selector)



    def onBet(self, betType, betName, betParam, value):
        dom = self.findLeagueDOM( betType, betName, betParam)
        dom.click()  # 选择kof
        self.div_showlimit().click() #弹出
        max = self.max_limit().text.replace(',', '')
        max = int(max)
        if value > max:
            print('资金不够下最高注', value, max)
            return False

        self.bet_gold_tt().click()

        vs = list(str(value))
        for v in vs:
            self.num_btn(v).click()

        gold = self.bet_gold2_tt().text.replace(',', '')
        gold = int(float(gold))
        if gold != value:
            print('金额异常', gold, value)
            return False
        self.betBtn_txt().click()
        time.sleep(1)
        b = self.orderMsg().text == '您已成功投注。'
        return True

    def orderMsg(self):  # 输入框
        return self.find_emelemt(By.ID, 'orderMsg')

    def bet_gold_tt(self):  # 输入框
        return self.find_emelemt(By.ID,'bet_gold_tt')

    def div_showlimit(self):  # 最大投注额按钮 点击后显示额度
        return self.find_emelemt(By.ID, 'div_showlimit')

    def max_limit(self):  # 最大投注额度
        return self.find_emelemt(By.ID, 'max_limit')

    def num_btn(self,num): # 点击键盘数字
        return self.find_emelemt(By.ID, 'num_' + str(num))

    def betBtn_txt(self):  # 下注的按钮
        return self.find_emelemt(By.ID, 'betBtn_txt')

    def bet_gold2_tt(self):  # 最后确认的金额
        return self.find_emelemt(By.ID, 'bet_gold2_tt')


