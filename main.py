# encoding: utf-8
# !/usr/bin/env python

import threading
import configparser
import datetime
import league_engine
from pages.hgw_pages.hgw_engine import HgwEngine
from pages.xjw_pages.xjw_engine import XjwEngine
import getpass
import time

datas = [
{
	'hgw':{
		'home': '勒沃库森',
		'away': '费雷堡',
		'started_at': 1614488400.0,
		'league': '德国甲组联赛',
		'bookmaker_league_id': 13477,
		'sport_id': 7,
		'home_id': 239482922699,
		'away_id': 239482920959,
		'team_home_id': 4080,
		'team_away_id': 4447,
		'team_away': 'Freiburg',
		'league_id': 3886,
		'league_name': 'Germany. Bundesliga',
		'updated_at': 1614335715,
		'swap_teams': False,
		'bookmaker_event_name': '勒沃库森 - 费雷堡',
		'bookmaker_league_name': '德国甲组联赛',
		'event_name': '勒沃库森 - 费雷堡',
		'team2_name': '费雷堡',
		'team1_name': '勒沃库森',
		'version': 1,
		'id': 'MTQwMTU2MjQwfDE5LDEuMCw1LDAsMCww',
		'koef': 1.71,
		'commission': 0,
		'diff': 0,
		'player': False,
		'corner': False,
		'bookmaker_event_id': 140156240,
		'event_id': 229302050,
		'bookmaker_id': 5,
		'period_id': 5,
		'bc_id': 470,
		'direct_link': '5806449471|1|null',
		'koef_lay': 0,
		'is_lay': 0,
		'market_depth': 0,
		'is_original': 1,
		'market_and_bet_type': 19,
		'market_and_bet_type_param': 1,
		'player1_id': 0,
		'player2_id': 0,
		'home_score': 0,
		'away_score': 0,
		'is_live': 0,
		'scanned_at': 1614348354877,
		'recorded_at': 1614348354877,
		'kafka_message_offset': 64119122460,
		'koef_last_modified_at': 1614335715247,
		'bookmaker_event_direct_link': '4696770',
		'val': 7046.783625730995,
		'bet_type_name': 19,
		'bet_name': '勒沃库森'
	}
},
{
	'hgw':{
		'home': '布加勒斯特迪纳摩',
		'away': '维托鲁康斯坦萨',
		'started_at': 1614321000.0,
		'league': '罗马尼亚甲组联赛',
		'bookmaker_league_id': 13515,
		'sport_id': 7,
		'home_id': 433021,
		'away_id': 1532242980,
		'team_home_id': 7979,
		'team_away_id': 7974,
		'team_away': 'Viitorul Constanta',
		'league_id': 4114,
		'league_name': 'Romania. Liga I',
		'updated_at': 1614348102,
		'swap_teams': False,
		'bookmaker_event_name': '布加勒斯特迪纳摩 - 维托鲁康斯坦萨',
		'bookmaker_league_name': '罗马尼亚甲组联赛',
		'event_name': '布加勒斯特迪纳摩 - 维托鲁康斯坦萨',
		'team2_name': '维托鲁康斯坦萨',
		'team1_name': '布加勒斯特迪纳摩',
		'version': 1,
		'id': 'MTQwMjA5MjAyfDE5LDAuNzUsNSwwLDAsMA',
		'koef': 1.86,
		'commission': 0,
		'diff': 1,
		'player': False,
		'corner': False,
		'bookmaker_event_id': 140209202,
		'event_id': 230043449,
		'bookmaker_id': 5,
		'period_id': 5,
		'bc_id': 469,
		'direct_link': '5828885166|0.5/1|null',
		'koef_lay': 0,
		'is_lay': 0,
		'market_depth': 0,
		'is_original': 1,
		'market_and_bet_type': 19,
		'market_and_bet_type_param': 0.75,
		'player1_id': 0,
		'player2_id': 0,
		'home_score': 0,
		'away_score': 0,
		'is_live': 0,
		'scanned_at': 1614348102928,
		'recorded_at': 1614348102929,
		'kafka_message_offset': 64118209683,
		'koef_last_modified_at': 1614348102877,
		'bookmaker_event_direct_link': '4712621',
		'val': 5913.978494623656,
		'bet_type_name': 19,
		'bet_name': '布加勒斯特迪纳摩'
	}
}
]


class MyTool:
    def __init__(self):
        self.dataEng = league_engine.LeagueEngine()
        self.xjwEng = XjwEngine()
        self.hgwEng = HgwEngine()

    def start_init(self):
        threading_hgw_init = self.hgwEng.threading_init()
        threading_xjw_init = self.xjwEng.threading_init()
        """目前这里需要手动，有验证码"""
        threading_hgw_init.join(999)
        threading_xjw_init.join(999)

        # """如若失败，重试一次"""
        # if not self.hgwEng.is_init:
        #     threading_hgw_init = self.hgwEng.threading_init()
        # if not self.xjwEng.is_init:
        #     threading_xjw_init = self.xjwEng.threading_init()
        #
        # threading_xjw_init.join(999)
        # threading_hgw_init.join(999)

        input('初始化完毕：双边正常进入Home后，按任意键继续')
        return True

    def testKoef(self):
        threading_hgw_init = self.hgwEng.threading_init()
        threading_hgw_init.join(999)
        while True:
            # data = self.dataEng.request_data2()
            for d in datas:
                print(d['hgw'])
                t1 = self.hgwEng.threading_getkoef(d)
                t1.join(300)
                print(self.hgwEng.koef)
                # input('Next for')

    def clear(self):
        self.xjwEng.koef = None
        self.hgwEng.koef = None

    def foreachKoef(self):
        while True:
            data = self.dataEng.request_data2()
            for d in data:
                self.start_koef(d)

    def start_koef(self, d):
        """
        双边查找比赛, 都有比赛都有koef的话就比较koef，再下单
        :param d:
        :return:
        """
        print(d)
        t1 = self.hgwEng.threading_getkoef(d)
        t2 = self.xjwEng.threading_getkoef(d)
        t1.join(300)
        t2.join(300)

        # """重试一次"""
        # if t1.is_alive():
        #     t1 = self.hgwEng.threading_getkoef(d)
        # if t2.is_alive():
        #     t2 = self.xjwEng.threading_getkoef(d)
        #
        # t1.join(300)
        # t2.join(300)
        if not self.hgwEng.koef:
            return False
        if not self.xjwEng.koef:
            return False
        hgwKof = self.hgwEng.koef
        xjwKof = self.xjwEng.koef
        xjwV = 100
        hgwV = 0
        if self.dataEng.koef_isok(hgwKof, xjwKof):
            hgwV = self.dataEng.get_value(hgwKof, xjwKof, xjwV)
            if self.xjwEng.xiazhu(d, xjwV):
                if self.hgwEng.xiazhu(d, hgwV):
                    print('下注成功')


if __name__ == '__main__':
    tool = MyTool()
    # tool.start_init()
    #
    # tool.foreachKoef()
    tool.testKoef()
