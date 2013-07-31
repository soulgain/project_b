# coding=utf-8

import pymongo

class FlightPriceDB(object):

    def __init__(self, host='127.0.0.1', port=1234):
        try:
            self.db = pymongo.MongoClient(host=host).flightPrice
            self.collection = self.db.testCollection
        except:
            print 'db fatal error'
            sys.exit(1)

    def insert(self, ent):
        self.collection.insert(ent)

    def dump(self, num=100):
        return list(self.collection.find(max=num))
