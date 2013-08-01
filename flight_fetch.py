# coding=utf-8

import crawler_ctrip
import crawler_quna
import crawler_sme
import time
import source


def startTask(dep, arr):
    crawler_quna.Crawler_quna(dep=dep, arr=arr).start()
    crawler_ctrip.Crawler_ctrip(dep=dep, arr=arr).start()
    #crawler_sme.Crawler_sme(dep=dep, arr=arr).start()


if __name__ == '__main__':
    while True:
        for task in source.tasks:
            startTask(dep=task['dep'], arr=task['arr'])

        for task in source.tasks:
            crawler_sme.Crawler_sme(dep=task['dep'], arr=task['arr']).start()

        time.sleep(source.interval)
