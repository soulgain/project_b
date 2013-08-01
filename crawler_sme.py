# coding=utf-8

import urllib
import urllib2
import json
import datetime
from data_model import LowestFlight
import source
import threading
import time


class Crawler_sme(object):
    def __init__(self, dep, arr):
        self.dep = dep
        self.arr = arr

    def start(self):
        date = datetime.date.today()
        delta = datetime.timedelta(days=1)
        days = 90
        current = 0
        threadList = []
        while current <= days:
            print current
            if threading.active_count() < 7:
                ct = CrawlerThread(self.dep, self.arr, date.isoformat())
                threadList.append(ct)
                ct.start()
                current += 1
                date += delta
            else:
                time.sleep(2)

        for t in threadList:
            if t.is_alive():
                print t
                t.join()
                print over


class CrawlerThread(threading.Thread):
    def __init__(self, dep, arr, date):
        threading.Thread.__init__(self)
        self.dep = dep
        self.arr = arr
        self.url = 'http://dev.ikamobile.com:8020/sme/employee/login.json'
        self.opener = None
        self.date = date
        self.daemon = True

    def run(self):
        self.login()
        url = 'http://dev.ikamobile.cn:8020/sme/flight.json?depCityCode=%s&arrCityCode=%s&depDate=%s&clientPlatformName=iPhone' % (source.smeCodeMap[self.dep], source.smeCodeMap[self.arr], self.date)
        doc = self.opener.open(url).read()
        jsonDic = json.loads(doc)
        priceList = []
        if cmp(jsonDic['code'], '0') == 0:
            for flight in jsonDic['data']['flights']:
                priceList.append(int(flight['lowestAdultCabinPrice']['ticketPrice']))
        price = self.lowestPrice(priceList)
        LowestFlight(dep=self.dep, arr=self.arr, fetchTime=datetime.datetime.now(), depDate=self.date, vendor='sme', price=str(price)).save()

    def lowestPrice(self, priceList):
        lowest = 10000
        for price in priceList:
            if price < lowest:
                lowest = price
        return lowest

    def login(self):
        url = 'http://dev.ikamobile.cn:8020/sme/employee/login.json'
        req = urllib2.Request(url)
        para = urllib.urlencode({'loginName':'15828545250', 'pwd':'000000', 'clientPlatformName':'iPhone'})
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
        ret = self.opener.open(req, para)
        #print ret.read()


if __name__ == '__main__':
    sme = Crawler_sme(dep='上海', arr='北京')
    sme.start()
