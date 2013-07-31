# coding=utf-8

import json
import urllib2
import re
import datetime
from data_model import LowestFlight


class Crawler_quna(object):
    def __init__(self, url):
        self.url = url

    def start(self):
        dic = json.loads(urllib2.urlopen(self.url).read())
        dic = dic['out']
        for ent in dic.viewkeys():
            LowestFlight(vendor='quna', flightName='', depDate=self.parseDate(ent), fetchTime=datetime.datetime.now(), price=dic[ent]['pr']).save()

    def parseDate(self, text):
        ret = re.search(r'[0-9]{4}-[0-9]{2}-[0-9]{2}', text)
        return ret.group(0)


def urlGen():
    return ['http://ws.qunar.com/all_lp.jcp?goDate=2013-08-02&from=北京&to=上海&output=json&count=30']

if __name__ == '__main__':
    for url in urlGen():
        Crawler_quna(url).start()
