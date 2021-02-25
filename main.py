# encoding: utf-8
# !/usr/bin/env python

import threading
import configparser
import datetime
import league_engine
from pages.hgw_pages.hgw_engine import HgwEngine
from pages.xjw_pages.xjw_engine import XjwEngine
import getpass

def updateTime(t):
    interval = datetime.timedelta(hours=12)
    d = datetime.datetime.fromtimestamp(t)
    d = d + interval
    return d.timestamp()


if __name__ == '__main__':
    dataEng = league_engine.LeagueEngine()
    xjwEng = XjwEngine()
    hgwEng = HgwEngine()

    itemPath = 'C:/Users/'+getpass.getuser()+'/Documents/GitHub/zuqiu/tmp/item_config.ini'
    itemConfig = configparser.ConfigParser()
    itemConfig.read(itemPath)

    def getItemName(name):
        h = itemConfig['name'].get(name)
        if not h:
            print('未找到对应的xjw队名')
            return name
        else:
            return h

    def hgw_init():
        hgwInit_thread = threading.Thread( target=hgwEng.onInit)
        hgwInit_thread.setDaemon(True)
        hgwInit_thread.start()
        return hgwInit_thread

    def xjw_init():
        hgwInit_thread = threading.Thread( target=xjwEng.onInit)
        hgwInit_thread.setDaemon(True)
        hgwInit_thread.start()
        return hgwInit_thread

    def xjw_getkoef(d):
        homeName = d['xjw']['home']
        awayName = d['xjw']['away']
        time = d['xjw']['started_at']
        kof = d['xjw']['koef']
        betType = d['xjw']['bet_type_name']
        betParam = d['xjw']['market_and_bet_type_param']
        betName = d['xjw']['bet_name']

        t = threading.Thread(target=xjwEng.getKof, args=(day, homeName, awayName, betType, betName, betParam))
        t.setDaemon(True)
        t.start()
        return t

    d = dataEng.test_data()
    print('init ing')
    # hinit = hgw_init()
    xinit = xjw_init()
    # hinit.join(30)
    xinit.join(999)
    while not xjwEng.is_init and xinit.is_alive():  # time out
        xjwEng.DV.quit()
        xinit = xjw_init()
        xinit.join(999)

    ######################################################################初始化结束
    # d = data[0]
    homeName = d['hgw']['home']
    awayName = d['hgw']['away']
    time = d['xjw']['started_at']
    kof = d['xjw']['koef']
    betType = d['xjw']['bet_type_name']
    betParam = d['xjw']['market_and_bet_type_param']
    betName = d['xjw']['bet_name']
    print(d['hgw'])  #网站Koef

    dt = datetime.datetime.fromtimestamp(time)
    day = dt.day

    homeName = getItemName(homeName)
    awayName = getItemName(awayName)

    t1 = xjw_getkoef(d)
    t1.join(300)

    # t1b = t1.is_alive()
    # while t1b or not xjwEng.koef:
    #     t1 = xjw_getkoef(d)
    #     t1.join(300)
    print(betName, xjwEng.koef)

