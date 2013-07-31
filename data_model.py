# coding=utf-8

from DBHandler import FlightPriceDB


class LowestFlight(object):

    def __init__(self, dep, arr, fetchTime, depDate, price, vendor):
        self.dep = dep
        self.arr = arr
        self.fetchTime = fetchTime
        self.depDate = depDate
        self.price = price
        self.vendor = vendor

    def save(self):
        dic = {}
        dic['dep'] = self.dep
        dic['arr'] = self.arr
        dic['fetchTime'] = self.fetchTime
        dic['depDate'] = self.depDate
        dic['price'] = self.price
        dic['vendor'] = self.vendor
        db = FlightPriceDB()
        db.insert(dic)
        #print self.__repr__()

    def __repr__(self):
        return self.vendor+'|'+self.dep+'->'+self.arr+'|'+self.depDate+'|'+self.price+'|'+repr(self.fetchTime)


if __name__ == '__main__':
    pass