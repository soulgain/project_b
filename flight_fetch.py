# coding=utf-8

import crawler_ctrip
import crawler_quna


def startTask():
    while True:
        crawler_quna.Crawler_quna().start()
        crawler_ctrip.Crawler_ctrip().start()


if __name__ == '__main__':
    startTask()
