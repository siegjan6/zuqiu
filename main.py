# encoding: utf-8
# !/usr/bin/env python

import hgw_request
import league_engine
import xjw_request

# hgwEngine = hgw_request.HgwRequest()
# hgwEngine.login()
#
legueEngine = league_engine.LeagueEngine()
#
data = legueEngine.test_data()
print(data)
# ary = hgwEngine.findLeagueToDetail(data['hgw'])


xjwEngine = xjw_request.XjwRequest()
xjwEngine.login()
xjwEngine.findLeagueToDetail(data)
