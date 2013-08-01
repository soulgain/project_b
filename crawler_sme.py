# coding=utf-8

import urllib
import urllib2
import json
import datetime
from data_model import LowestFlight
import source


class Crawler_sme(object):
    def __init__(self, dep, arr):
        self.dep = dep
        self.arr = arr
        self.url = 'http://dev.ikamobile.com:8020/sme/employee/login.json'
        self.opener = None

    def login(self):
        url = 'http://dev.ikamobile.cn:8020/sme/employee/login.json'
        req = urllib2.Request(url)
        para = urllib.urlencode({'loginName':'15828545250', 'pwd':'000000', 'clientPlatformName':'iPhone'})
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
        ret = self.opener.open(req, para)
        print ret.read()

    def start(self):
        date = datetime.date.today()
        delta = datetime.timedelta(days=1)
        for x in xrange(0,90):
            self.fetchWithDate(date.isoformat())
            date += delta

    def fetchWithDate(self, date):
        url = 'http://dev.ikamobile.cn:8020/sme/flight.json?depCityCode=%s&arrCityCode=%s&depDate=%s&clientPlatformName=iPhone' % (source.smeCodeMap[self.dep], source.smeCodeMap[self.arr], date)
        doc = self.opener.open(url).read()
        jsonDic = json.loads(doc)
        priceList = []
        if cmp(jsonDic['code'], '0') == 0:
            for flight in jsonDic['data']['flights']:
                priceList.append(int(flight['lowestAdultCabinPrice']['ticketPrice']))
        price = self.lowestPrice(priceList)
        LowestFlight(dep=self.dep, arr=self.arr, fetchTime=datetime.datetime.now(), depDate=date, vendor='sme', price=str(price)).save()

    def lowestPrice(self, priceList):
        lowest = 10000
        for price in priceList:
            if price < lowest:
                lowest = price
        return lowest


if __name__ == '__main__':
    sme = Crawler_sme(dep='上海', arr='北京')
    sme.login()
    sme.start()
