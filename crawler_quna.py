# coding=utf-8

import json
import urllib2
import datetime
from data_model import LowestFlight


class Crawler_quna(object):
    def __init__(self, dep, arr, date=datetime.date.today().isoformat()):
        self.url = 'http://ws.qunar.com/all_lp.jcp?goDate=%s&from=%s&to=%s&output=json&count=30'
        self.dep = dep
        self.arr = arr
        self.date = date

    def start(self):
        dic = json.loads(urllib2.urlopen(self.url % (self.date, self.dep, self.arr)).read())
        dic = dic['out']
        for ent in dic.viewkeys():
            #date = re.search(r'([0-9]{4})-([0-9]{2})-([0-9]{2})', dic[ent]['dt'])
            #LowestFlight(vendor='quna', flightName='', depDate=datetime.date(int(date.group(1)), int(date.group(2)), int(date.group(3))), fetchTime=datetime.datetime.now(), price=dic[ent]['pr']).save()
            LowestFlight(vendor='quna', dep=self.dep, arr=self.arr, depDate=dic[ent]['dt'], fetchTime=datetime.datetime.now(), price=dic[ent]['pr']).save()


if __name__ == '__main__':
    Crawler_quna(dep='上海', arr='北京').start()
