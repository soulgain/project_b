# coding=utf-8

import urllib
import urllib2
import json
import datetime
from data_model import LowestFlight
import source
import threading
import time

hostName = 'http://sme.ikamobile.com'

class Crawler_sme(object):
    def __init__(self, dep, arr):
        self.dep = dep
        self.arr = arr

    def start(self):
        date = datetime.date.today()
        delta = datetime.timedelta(days=1)
        days = 90
        current = 0
        threadLimit = 10
        threadList = []
        while current <= days:
            print current
            if threading.active_count() < threadLimit:
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
                print 'over'


class CrawlerThread(threading.Thread):
    def __init__(self, dep, arr, date):
        threading.Thread.__init__(self)
        self.dep = dep
        self.arr = arr
        self.url = hostName + '/sme/employee/login.json'
        self.opener = None
        self.date = date
        self.daemon = True

    def run(self):
        try:
            if self.login() == False:
                return
        except Exception, e:
            print e
            return
        
        url = hostName + '/sme/flight.json?depCityCode=%s&arrCityCode=%s&depDate=%s&clientPlatformName=iPhone' % (source.smeCodeMap[self.dep], source.smeCodeMap[self.arr], self.date)
        try:
            doc = self.opener.open(url, timeout=30).read()
        except Exception, e:
            if cmp(repr(e), 'timed out') == 0:
                self.run()
            else:
                return
        
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
        url = hostName + '/sme/employee/login.json'
        req = urllib2.Request(url)
        para = urllib.urlencode({'loginName':'15198065309', 'pwd':'111111', 'clientPlatformName':'iPhone'})
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
        ret = None
        try:
            ret = self.opener.open(req, para, timeout=30)
        except Exception, e:
            if cmp(repr(e), 'timed out') == 0:
                self.login()
        jsonDic = json.loads(ret.read())
        if cmp(jsonDic['code'], '0') != 0:
            return False
        
        #print ret.read()


if __name__ == '__main__':
    Crawler_sme(dep='上海', arr='北京').start()
