# coding=utf-8

import crawler_ctrip
import crawler_quna
import time
import source


def startTask(dep, arr):
    while True:
        crawler_quna.Crawler_quna(dep=dep, arr=arr).start()
        crawler_ctrip.Crawler_ctrip(dep=dep, arr=arr).start()
        time.sleep(10*60)

if __name__ == '__main__':
    for task in source.tasks:
        startTask(dep=task['dep'], arr=task['arr'])
