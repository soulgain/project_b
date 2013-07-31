# coding=utf-8

from bs4 import BeautifulSoup
import urllib2
import re
import datetime

from data_model import LowestFlight


class Crawler_ctrip(object):
    def __init__(self, dep, arr):
        self.dep = dep
        self.arr = arr
        self.url = 'http://flights.ctrip.com/booking/%s-%s-day-1.html'

    def start(self):
        global g_codeMap
        html = urllib2.urlopen(self.url % (g_codeMap[self.dep], g_codeMap[self.arr]), 'html5lib', timeout=30).read()
        print self.url, ' - OK'
        soup = BeautifulSoup(html)
        lis = soup.find_all(id='lowestPriceDateList')[0].find_all('li')
        for li in lis:
            priceTag = li.strong
            if priceTag:
                date = self.parseDate(li['onclick'])
                price = priceTag.text
                LowestFlight(vendor='ctrip', dep=self.dep, arr=self.arr, price=price, depDate=date, fetchTime=datetime.datetime.now()).save()

    def parseDate(self, tagText):
        ret = re.search(r'[0-9]{4}-[0-9]{2}-[0-9]{2}', tagText)
        return ret.group(0)

g_codeMap = {'北京':'BJS', '上海':'SHA'}

if __name__ == '__main__':
    Crawler_ctrip(dep='北京', arr='上海').start()
