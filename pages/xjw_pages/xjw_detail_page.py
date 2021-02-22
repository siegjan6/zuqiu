from pages.base_page import BasePage
from selenium.webdriver.common.by import By



class XjwDetialPage(BasePage):
    """
    登录页
    """
    def _types(self):
        return self.find_emelemts((By.CLASS_NAME, 'bettype'))

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
                    name,
                    vs
                }
                ret_types.append(ret_cell)
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

        if betType == 19:  # 找球队名称 17是+的，18是-的，数据网没有+号 为0就没有正负号
            datas = self.updateData()[0]
            for item in datas:
                if item['name'] == '大':  # 大
                    if betParam in item['vs'].keys():
                        return item['vs'][betParam]

        if betType == 20:  # 找球队名称 17是+的，18是-的，数据网没有+号 为0就没有正负号
            datas = self.updateData()[0]
            for item in datas:
                if item['name'] == '小':  # 小
                    if betParam in item['vs'].keys():
                        return item['vs'][betParam]

    def findLeagueDOM(self, betType, betName, betParam):
        self._findLeague(betType, betName, betParam)[0]

    def findLeagueKof(self, betType, betName, betParam):
        self._findLeague(betType, betName, betParam)[1]












