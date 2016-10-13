#!/usr/bin/env python3
# coding=utf-8
import requests
import re
import sys

reload(sys)
sys.setdefaultencoding("utf-8")


class spider():
    def __init__(self):
        print '开始爬虫了!!!'

    def changePage(self, url, nums):
        nowPage = int(re.search('/0-(\d+)/', url, re.S).group(1))
        appendPage = []

        for num in range(nowPage, nums + 1):
            nextPageUrl = re.sub('/0-(\d+)/', '/0-%s/' % num, url, re.S)
            appendPage.append(nextPageUrl)

        return appendPage

    def getSource(self, url):
        html = requests.get(url)
        return html.text

    def matchUl(self, html):
        Ul = re.search('<ul class="zy_course_list">(.*?)</ul>', html, re.S).group(1)
        return Ul

    def matchLi(self, ul):
        li = re.findall('<li>(.*?)</li>', ul, re.S)
        return li

    def getInfo(self, li):
        info = {}
        info['title'] = re.search('<a title="(.*?)"', li, re.S).group(1)
        info['people'] = re.search('<p class="color99">(.*?)</p>', li, re.S).group(1)
        return info

    def saveInfo(self, infos):
        file = open('info.txt', 'a')

        for info in infos:
            file.writelines('title : ' + info['title'] + '\n')
            file.writelines('people : ' + info['people'] + '\n\n')

        file.close()


if __name__ == "__main__":
    url = 'http://www.maiziedu.com/course/list/all-all/0-1/'
    result = []
    spider = spider();
    all_url = spider.changePage(url, 30)
    for each in all_url:
        html = spider.getSource(url)
        htmlMatchUl = spider.matchUl(html)
        htmlMatchLi = spider.matchLi(htmlMatchUl)
        for each in htmlMatchLi:
            info = spider.getInfo(each)
            result.append(info)

    spider.saveInfo(result)
