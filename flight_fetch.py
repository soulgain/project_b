# coding=utf-8

import crawler_ctrip
import crawler_quna
import time


def startTask():
    while True:
        crawler_quna.Crawler_quna().start()
        crawler_ctrip.Crawler_ctrip().start()
        time.sleep(10*60)

if __name__ == '__main__':
    startTask()
