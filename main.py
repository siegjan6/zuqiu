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

def updateTime(t):
    interval = datetime.timedelta(hours=12)
    d = datetime.datetime.fromtimestamp(t)
    d = d + interval
    return d.timestamp()


def findKof(d):
    homeName = d['hgw']['home']
    awayName = d['hgw']['away']
    time = d['xjw']['started_at']
    kof = d['xjw']['koef']
    betType = d['xjw']['bet_type_name']
    betParam = d['xjw']['market_and_bet_type_param']
    betName = d['xjw']['bet_name']

    homeName = getItemName(homeName)
    awayName = getItemName(awayName)
    if not homeName or not awayName:
        return
    if isErrorLeague(homeName, awayName):
        return
    d['hgw']['home'] = homeName
    d['hgw']['away'] = awayName

    print(d)  # 网站Koef
    print('找到队名，开始找比赛',homeName,awayName)
    t1 = xjw_getkoef(d)
    t1.join(300)
    if t1.is_alive():
        addErrorLeague(homeName, awayName)
    elif not xjwEng.koef :
        addErrorLeague(homeName, awayName)
    # t1b = t1.is_alive()
    # while t1b or not xjwEng.koef:
    #     t1 = xjw_getkoef(d)
    #     t1.join(300)

    print(betName, kof, xjwEng.koef)
    xjwEng.koef = None  #用完后置空


def xjw_getkoef(d):
    homeName = d['hgw']['home']  # 此处需要用Hgw的队名
    awayName = d['hgw']['away']  # 此处需要用Hgw的队名
    time = d['xjw']['started_at']
    kof = d['xjw']['koef']
    betType = d['xjw']['bet_type_name']
    betParam = d['xjw']['market_and_bet_type_param']
    betName = d['xjw']['bet_name']

    dt = datetime.datetime.fromtimestamp(time)
    day = dt.day

    t = threading.Thread(target=xjwEng.getKof, args=(day, homeName, awayName, betType, betName, betParam))
    t.setDaemon(True)
    t.start()
    return t


isErrLeague = {}
def addErrorLeague(home,away):
    if home+away in isErrLeague:
        isErrLeague[home+away] = isErrLeague[home+away] + 1
    else:
        isErrLeague[home + away] = 1

def isErrorLeague(home,away):
    if home+away in isErrLeague:
        return isErrLeague[home+away]
    else:
        return None


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
            # print('未找到对应的xjw队名')
            return None
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

    data = []
    while True:
        newData = dataEng.request_data2()
        if data != newData:
            data = newData
            for d in data:
                findKof(d)
        else:
            time.sleep(20)

