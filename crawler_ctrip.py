# coding=utf-8

from bs4 import BeautifulSoup
import urllib2
import re
import datetime

from data_model import LowestFlight


class Crawler_ctrip(object):
    def __init__(self, url, db=None):
        self.url = url
        self.db = db

    def start(self):
        html = urllib2.urlopen(self.url, 'html5lib', timeout=30).read()
        print self.url, ' - OK'
        soup = BeautifulSoup(html)
        lis = soup.find_all(id='lowestPriceDateList')[0].find_all('li')
        for li in lis:
            priceTag = li.strong
            if priceTag:
                date = self.parseDate(li['onclick'])
                price = priceTag.text
                LowestFlight(vendor='ctrip', flightName='', price=price, depDate=date, fetchTime=datetime.datetime.now()).save()

    def parseDate(self, tagText):
        ret = re.search(r'[0-9]{4}-[0-9]{2}-[0-9]{2}', tagText)
        return ret.group(0)


def urlGen():
    urls = ['http://flights.ctrip.com/booking/SHA-BJS-day-1.html']
    return urls


if __name__ == '__main__':
    for url in urlGen():
        Crawler_ctrip(url).start()
