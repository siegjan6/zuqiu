from pages.base_page import BasePage
from selenium.webdriver.common.by import By



class XjwDetialPage(BasePage):
    """
    登录页
    """
    def _types(self):
        return self.find_emelemts(By.CLASS_NAME, 'bettype')

    def typeDom(self, betTypeNum):
        """
        找到type的DOM，（盘分，大小）
        :param betTypeNum: 17,18,19,20
        :return: DOM  .text'墨尔本胜利\n-0.25\n1.11\n0\n0.78\n+0.25\n0.58'
        """
        if betTypeNum in (17, 18):
            return self._types()[0]
        if betTypeNum in (19, 20):
            return self._types()[1]

    def bettype_items(self, betTypeNum):
        return self.typeDom(betTypeNum).find_elements_by_class_name('bettype_item')

    def comkeypad_lefttop(self):
        return self.find_emelemt(By.CLASS_NAME, 'comkeypad_lefttop')

    def comkeypad_item(self, v):
        i = int(v) - 1
        if i == -1:
            i = 9
        items = self.comkeypad_lefttop().find_elements_by_class_name('comkeypad_item')
        print(items[i].text)
        return items[i]

    def onClickKeypad(self, value):
        valueary = list(str(value))
        for v in valueary:
            e = self.comkeypad_item(v)
            self.click(e)

    def comtickets_value(self):
        """
        可用资金
        :return:
        """
        return self.find_emelemt(By.CLASS_NAME, 'comtickets_value')

    def textfield_input_value(self):
        """
        输入的金额
        :return:number
        """
        txt = self.find_emelemt(By.CLASS_NAME, 'textfield_input').text
        t = txt.replace(',','')
        return int(t)

    def comBtn(self):
        return self.find_emelemt(By.ID, 'comBtn')

    def keypadDark(self):
        """
        点击最高
        :return:
        """
        return self.find_emelemt(By.CLASS_NAME, 'keypad-dark')

    def updateData(self):
        """

        :return:
        [0,
            [
            {
                name,
                vs:
                {
                    pank:
                        [r,kof]
                }
            }
            ,]
        1]
        """
        ret_types = []
        types = self._types()[0:2]
        for type_element in types:  # 盘分 和  大小
            ret_typeData = []
            items = type_element.find_elements_by_class_name('bettype_item')
            for item in items:  # '墨尔本胜利\n-0.25\n1.11\n0\n0.78\n+0.25\n0.58'
                ds = item.text.replace('+', '').split('\n')
                name = ds[0]
                vs = {}
                length = int((len(ds) - 1) / 2)
                for i in range(length):
                    pank = ds[i * 2 + 1]
                    kof = ds[i * 2 + 2]
                    r = item.find_elements_by_class_name('bettype_oddsbox')[i]
                    vs[pank] = [r, kof]
                ret_cell = {
                    'name': name,
                    'vs': vs
                }
                ret_typeData.append(ret_cell)
            ret_types.append(ret_typeData)
        return ret_types

    def _findLeague(self, betType, betName, betParam):
        """

        :param betType: 17,18,19,20
        :param betName: 要打的队名，
        :param betParam: 盘口 1.25
        :return:
        """
        if betType == 17:  # 找球队名称 17是+的，18是-的，数据网没有+号 为0就没有正负号
            datas = self.updateData()[0]
            for item in datas:
                if item['name'] == betName:  # 找到队名
                    if betParam in item['vs'].keys():
                        return item['vs'][betParam]

        if betType == 18:  # 找球队名称 17是+的，18是-的，数据网没有+号 为0就没有正负号
            datas = self.updateData()[0]
            for item in datas:
                if item['name'] == betName:  # 找到队名
                    if betParam in item['vs'].keys():
                        return item['vs'][betParam]

        if betType == 19:  #
            datas = self.updateData()[1]
            for item in datas:
                if item['name'] == '大':  # 大
                    if betParam in item['vs'].keys():
                        return item['vs'][betParam]

        if betType == 20:  #
            datas = self.updateData()[1]
            for item in datas:
                if item['name'] == '小':  # 小
                    if betParam in item['vs'].keys():
                        return item['vs'][betParam]

    def findLeagueDOM(self, betType, betName, betParam):
        return self._findLeague(betType, betName, betParam)[0]

    def findLeagueKof(self, betType, betName, betParam):
        return self._findLeague(betType, betName, betParam)[1]


    def getDarkValue(self):
        """
        最高下注
        :return:
        """
        e = self.find_emelemt(By.CLASS_NAME,'textfield-stake')
        tx = e.find_element_by_class_name('comtickets_value').text
        ary = tx.split(' ')
        v = ary[-1].replace(',', '')
        print(v)
        return int(v)

    def getUsableValue(self):
        """
        可用资金
        :return:
        """
        e = self.find_emelemts(By.CLASS_NAME, 'comtickets_item')[0]
        txt = e.text.split('\n')[-1].replace('.', '')
        return int(txt)

    def onBet(self, betType, betName, betParam, value):
        e = self.findLeagueDOM(betType, betName, betParam)
        self.click(e) #打开下注键盘

        isAlert = self.is_alert()
        if isAlert:
            return False

        dark = self.getDarkValue()
        usable = self.getUsableValue()

        if value > usable:
            print('资金不够下注', value, usable)
            return False
        if value > dark:
            print('资金不够下最高注', value, dark)

        self.onClickKeypad(value)  # 按金额

        input_v = self.textfield_input_value()

        if input_v == value:
            self.click(self.comBtn())
            return True
        else:
            print('金额异常', input_v, value)
            return False









