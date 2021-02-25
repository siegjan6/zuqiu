# encoding: utf-8
# !/usr/bin/env python

import threading
import league_engine
from pages.hgw_pages.hgw_engine import HgwEngine
from pages.xjw_pages.xjw_engine import XjwEngine



if __name__ == '__main__':
    dataEng = league_engine.LeagueEngine()
    xjwEng = XjwEngine()
    hgwEng = HgwEngine()

    def init_hgw():
        hgwInit_thread = threading.Thread( target=hgwEng.onInit)
        hgwInit_thread.start()
        return hgwInit_thread

    def init_xjw():
        hgwInit_thread = threading.Thread( target=xjwEng.onInit)
        hgwInit_thread.start()
        return hgwInit_thread

    data = dataEng.request_data()
    print ('init ing')
    hinit = init_hgw()
    xinit = init_xjw()
    hinit.join(30)
    xinit.join(30)
    print('data eng', data)