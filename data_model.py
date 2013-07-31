# coding=utf-8

from DBHandler import FlightPriceDB


class LowestFlight(object):

    def __init__(self, flightName, fetchTime, depDate, price, vendor):
        self.flightName = flightName
        self.fetchTime = fetchTime
        self.depDate = depDate
        self.price = price
        self.vendor = vendor

    def save(self):
        dic = {}
        dic['flightName'] = self.flightName
        dic['fetchTime'] = self.fetchTime
        dic['depDate'] = self.depDate
        dic['price'] = self.price
        dic['vendor'] = self.vendor
        db = FlightPriceDB()
        db.insert(dic)
        print self.__repr__()

    def __repr__(self):
        return self.vendor+'|'+self.flightName+'|'+self.depDate+'|'+self.price+'|'+repr(self.fetchTime)
