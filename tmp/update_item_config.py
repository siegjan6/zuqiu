# encoding: utf-8
# !/usr/bin/env python
import configparser


def updateTempIniToItemIni():
    path = 'temp.ini'
    savePath = 'item_config.ini'
    config = configparser.ConfigParser()
    config.read(path, encoding='utf-8')

    section = config['name']

    saveConfig = configparser.ConfigParser()
    saveConfig.read(savePath, encoding='utf-8')

    vvv = ','.join(section.keys())
    keys = vvv.split(',')
    len = len(keys)
    for i in range(len):
        ary = keys[i]
        hgwName = ary[1]
        xjwName = ary[2]
        saveConfig.set('name', hgwName, xjwName)
    saveConfig.write(open(savePath, 'w'))

savePath = 'item_config.ini'
saveConfig = configparser.ConfigParser()
saveConfig.read(savePath)
values = ','.join(saveConfig['name'].values())
values = values.split(',')
print(values)