# coding=utf-8

import pymongo
import sys

class FlightPriceDB(object):

    def __init__(self, host='127.0.0.1', port=1234):
        try:
            self.db = pymongo.MongoClient(host=host, port=1234).flightPrice
            self.collection = self.db.testCollection
        except Exception, e:
            print 'db fatal error',e
            sys.exit(1)

    def insert(self, ent):
        self.collection.insert(ent)

    def dump(self, num=100):
        return list(self.collection.find(max=num))


if __name__ == '__main__':
    FlightPriceDB()