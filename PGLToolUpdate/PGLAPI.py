#!/usr/bin/env python

import json
import requests
import os
import time
import sys


def getLoginStatus():
    url = 'http://3ds.pokemon-gl.com/frontendApi/getLoginStatus'
    data = {}
    data['languageId'] = '2'
    data['timezone'] = 'Europe/London'

    header = {}
    header['Host'] = '3ds.pokemon-gl.com'
    header['Origin'] = 'http://3ds.pokemon-gl.com'
    header['Referer'] = 'http://3ds.pokemon-gl.com/battle/oras'
    header['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'

    r = requests.post(url, headers=header, data=data)
    return r.cookies


def getSeason(generationId, cookies):

    url = 'http://3ds.pokemon-gl.com/frontendApi/gbu/getSeason'

    data = {}
    data['languageId'] = '2'
    # 1 for xy, 2 for oras
    data['generationId'] = generationId
    data['timezone'] = 'EST'

    header = {}
    header['Host'] = '3ds.pokemon-gl.com'
    header['Origin'] = 'http://3ds.pokemon-gl.com'

    if generationId == '1':
        header['Referer'] = 'http://3ds.pokemon-gl.com/battle/xy'
    else:
        header['Referer'] = 'http://3ds.pokemon-gl.com/battle/oras'

    header['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'

    r = requests.post(url, headers=header, data=data, cookies=cookies)
    s = json.loads(r.text)
    return s['seasonInfo'][0]['seasonId'], (str(s['seasonInfo'][0]['seasonName']).split(' '))[1]


def getUpdatedTime(generationId, seasonId, seasonName):

    url = 'http://3ds.pokemon-gl.com/frontendApi/gbu/getSeasonPokemon'

    data = {}
    data['languageId'] = '2'
    # 1 for xy, 2 for oras
    data['seasonId'] = str(seasonId)
    data['battleType'] = 0
    data['timezone'] = 'GMT'
    # print data

    header = {}
    header['Host'] = '3ds.pokemon-gl.com'
    header['Origin'] = 'http://3ds.pokemon-gl.com'

    if generationId == '1':
        header['Referer'] = 'http://3ds.pokemon-gl.com/battle/xy'
    else:
        header['Referer'] = 'http://3ds.pokemon-gl.com/battle/oras'

    header['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'

    r = requests.post(url, headers=header, data=data)
    s = json.loads(r.text)

    if generationId == '1':
        return "xy" + "-" + seasonName + "-" + str(s['updateDate']).replace(' ', '-').replace('/', '').replace(':', '') + '.mdb'
    else:
        return "oras" + "-" + seasonName + "-" + str(s['updateDate']).replace(' ', '-').replace('/', '').replace(':', '') + '.mdb'


def getSeasonPokemonDetail(generationId, seasonId, pkId, battleType):

    url = 'http://3ds.pokemon-gl.com/frontendApi/gbu/getSeasonPokemonDetail'

    data = {}

    data['languageId'] = '2'
    data['seasonId'] = str(seasonId)
    data['battleType'] = str(battleType)

    data['timezone'] = 'EST'
    data['pokemonId'] = pkId
    data['displayNumberWaza'] = '20'
    data['displayNumberTokusei'] = '3'
    data['displayNumberSeikaku'] = '3'
    data['displayNumberItem'] = '3'
    data['displayNumberLevel'] = '10'
    data['displayNumberPokemonIn'] = '1'
    data['displayNumberPokemonDown'] = '1'
    data['displayNumberPokemonDownWaza'] = '1'

    header = {}
    header['Host'] = '3ds.pokemon-gl.com'
    header['Origin'] = 'http://3ds.pokemon-gl.com'

    if generationId == '1':
        header['Referer'] = 'http://3ds.pokemon-gl.com/battle/xy'
    else:
        header['Referer'] = 'http://3ds.pokemon-gl.com/battle/oras'

    header['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'

    r = requests.post(url, headers=header, data=data)
    return r.text


def setupSql(pkIdStr, battleType, jsonText):
    seasonPokemonDetail = json.loads(jsonText)
    pkIdStr = str(pkIdStr).replace('-', '.')
    ranking = str(seasonPokemonDetail["rankingPokemonInfo"]["ranking"])
    if ranking == '0':
        return ''
    moveName = ['-'] * 20
    moveType = ['-1'] * 20
    moveUsage = ['0'] * 20
    itemName = ['-'] * 3
    itemUsage = ['0'] * 3
    abilityName = ['-'] * 3
    abilityUsage = ['0'] * 3
    natureName = ['-'] * 3
    natureUsage = ['0'] * 3

    wazaInfo = seasonPokemonDetail["rankingPokemonTrend"]["wazaInfo"]
    if wazaInfo != None:
        listSize = len(wazaInfo)
        if listSize > 20:
            listSize = 20
        for i in range(0, listSize):
            moveName[i] = wazaInfo[i]["name"]
            moveType[i] = wazaInfo[i]["typeId"]
            moveUsage[i] = wazaInfo[i]["usageRate"]

    itemInfo = seasonPokemonDetail["rankingPokemonTrend"]["itemInfo"]
    if itemInfo != None:
        listSize = len(itemInfo)
        if listSize > 3:
            listSize = 3
        for i in range(0, listSize):
            itemName[i] = itemInfo[i]["name"]
            itemUsage[i] = itemInfo[i]["usageRate"]

    tokuseiInfo = seasonPokemonDetail["rankingPokemonTrend"]["tokuseiInfo"]
    if tokuseiInfo != None:
        listSize = len(tokuseiInfo)
        if listSize > 3:
            listSize = 3
        for i in range(0, listSize):
            abilityName[i] = tokuseiInfo[i]["name"]
            abilityUsage[i] = tokuseiInfo[i]["usageRate"]

    seikakuInfo = seasonPokemonDetail["rankingPokemonTrend"]["seikakuInfo"]
    if seikakuInfo != None:
        listSize = len(seikakuInfo)
        if listSize > 3:
            listSize = 3
        for i in range(0, listSize):
            natureName[i] = seikakuInfo[i]["name"]
            natureUsage[i] = seikakuInfo[i]["usageRate"]

    sql = "insert into battleType" + str(battleType) + " values("
    sql += pkIdStr + ","
    sql += str(ranking) + ","

    for i in range(0, 3):
        sql += "'" + abilityName[i] + "',"
        sql += str(abilityUsage[i]) + ","
    for i in range(0, 3):
        sql += "'" + natureName[i] + "',"
        sql += str(natureUsage[i]) + ","
    for i in range(0, 3):
        sql += "'" + str(itemName[i]).replace("'", "''") + "',"
        sql += str(itemUsage[i]) + ","

    for i in range(0, 19):
        sql += "'" + str(moveName[i]).replace("'", "''") + "',"
        sql += str(moveType[i]) + ","
        sql += str(moveUsage[i]) + ","

    sql += "'" + str(moveName[19]).replace("'", "''") + "',"
    sql += str(moveType[19]) + ","
    sql += str(moveUsage[19]) + ")"
    return sql




'''

path = '/home/ubuntu/PGLDataUpdate/'

f = open(path + 'xyVer.txt', 'r')
xyVer = str(f.readline()).strip()
f.close()
f = open(path + 'orasVer.txt', 'r')
orasVer = str(f.readline()).strip()
f.close()
f = open(path + 'pokeIdList.dat', 'r')
pkList = f.readlines()
f.close()
f = open(path + 'PGLDataLog', 'a')
ISOTIMEFORMAT = '%Y-%m-%d %X'
f.write(time.strftime(ISOTIMEFORMAT, time.localtime(time.time())) + '\n')

cookies = getLoginStatus()

try:
    seasonId, seasonName = getSeason('1', cookies)
except:
    f.write('PGL is under maintaining.\n')
    sys.exit()
newXY = getUpdatedTime('1', seasonId, seasonName)
if newXY == xyVer:
    f.write('no new data\n')
else:
    os.mkdir(path + 'CurrentSeason/xy/' + newXY)
    f.write(newXY + '\n')
    for i in range(0, 6):
        nf = open(path + 'CurrentSeason/xy/' +
                  newXY + '/' + str(i) + '.txt', 'w')
        for pkId in pkList:
            pkId = str(pkId).strip()
            detail = getSeasonPokemonDetail('1', seasonId, pkId, i)
            sql = setupSql(pkId, i, detail)
            if sql != '':
                nf.write(str(sql) + '\n')
        nf.close()

    f1 = open(path + 'xyVer.txt', 'w')
    f1.write(newXY)
    f1.close()


seasonId, seasonName = getSeason('2', cookies)
newORAS = getUpdatedTime('2', seasonId, seasonName)

if newORAS == orasVer:
    f.write('no new data\n')
else:
    os.mkdir(path + 'CurrentSeason/oras/' + newORAS)
    f.write(newORAS + '\n')
    for i in range(0, 6):
        nf = open(path + 'CurrentSeason/oras/' + newORAS + '/' + str(i) + '.txt', 'w')
        for pkId in pkList:
            pkId = str(pkId).strip()
            detail = getSeasonPokemonDetail('2', seasonId, pkId, i)
            sql = setupSql(pkId, i, detail)
            if sql != '':
                nf.write(str(sql) + '\n')
        nf.close()

    f1 = open(path + 'orasVer.txt', 'w')
    f1.write(newORAS)
    f1.close()

f2 = open(path + 'CurrentSeason/checkUpdate.txt', 'w')
f2.write(newXY + '\n')
f2.write(newORAS)
f2.close()


f1 = open(path + 'seasonName.txt', 'r')
oldSeasonName = str(f1.readline()).strip()
f1.close()

if seasonName != oldSeasonName:

    newXY = getUpdatedTime('1', oldSeasonName, oldSeasonName)
    os.mkdir(path + 'HistoryRepo/tempXy/' + newXY)
    f.write('change season, old last version:' + newXY + '\n')
    for i in range(0, 6):
        nf = open(path + 'HistoryRepo/tempXy/' + newXY + '/' + str(i) + '.txt', 'w')
        for pkId in pkList:
            pkId=str(pkId).strip()
            detail=getSeasonPokemonDetail('1', seasonId, pkId, i)
            sql=setupSql(pkId, i, detail)
            if sql != '':
                nf.write(str(sql) + '\n')
        nf.close()

    newORAS=getUpdatedTime('2', '1' + oldSeasonName, oldSeasonName)
    os.mkdir(path + 'HistoryRepo/tempOras/' + newORAS)
    f.write('change season, old last version:' + newORAS + '\n')
    for i in range(0, 6):
        nf=open(path + 'HistoryRepo/tempOras/' + newORAS + '/' + str(i) + '.txt', 'w')
        for pkId in pkList:
            pkId=str(pkId).strip()
            detail=getSeasonPokemonDetail('2', seasonId, pkId, i)
            sql=setupSql(pkId, i, detail)
            if sql != '':
                nf.write(str(sql) + '\n')
        nf.close()

    f1=open(path + 'seasonName.txt', 'w')
    f1.write(seasonName)
    f1.close()

    f2=open(path + 'HistoryRepo/xy-historyList.txt', 'a')
    f2.write(newXY)
    f2.close()
    f2=open(path + 'HistoryRepo/oras-historyList.txt', 'a')
    f2.write(newORAS)
    f2.close()

f.close()
'''

os.system('/home/ubuntu/DearUnknown/PGLToolUpdate/PGLToolUpdate/pushToRemote.sh')
