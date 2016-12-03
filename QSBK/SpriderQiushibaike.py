#!/usr/bin/env python2.7
# -*- coding:utf-8 -*-
#
#1.都一次完成时间2016年12月2日，版本号version0.1
#    网络爬虫：获取糗事百科上的段子，并显示段子的发布人及点赞个数(此版本不能读取图片)
#    回车键下一条段子，q键确定退出
#

__author__ = 'peng'

import urllib
import urllib2
import re
#import thread
#import time

#糗事百科爬虫类
class QSBK:

    #初始化
    def __init__(self):
        #页面索引
        self.pageIndex = 1
        #模拟浏览器
        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5;Windows NT)'
        #初始化header
        self.headers = { 'User-Agent' : self.user_agent}
        #存放段子的变量，每个变量存放一页的段子
        self.stories = []
        #存放程序状态变量
        self.enable = False

    #传入页面索引获取页面代码
    def getPageCode(self,pageIndex):
        try:
            url = 'http://www.qiushibaike.com/hot/page/' + str(pageIndex)
            #构建请求的request
            request = urllib2.Request(url,headers = self.headers)
            #利用urlopen获取页面代码
            response = urllib2.urlopen(request)
            #将页面转化为UTF-8编码
            pageCode = response.read().decode('utf-8')
            return pageCode

        except urllib2.URLError, e:
            if hasattr(e,"reason"):
                print u"连接糗事百科失败,错误原因",e.reason
                return None

     #传入页面代码，返回本页不带图片的段子列表
    def getPageItems(self,pageIndex):
        pageCode = self.getPageCode(pageIndex)
        if not pageCode:
            print u"页面加载失败...."
            return None
        #正则表达式匹配
        pattern = re.compile('<div class="author clearfix">.*?href.*?<img src.*?title=.*?<h2>(.*?)</h2>.*?<div class="content">.*?<span>(.*?)</span>.*?</div>.*?<i class="number">(.*?)</i>',re.S)
        #存储每页内容
        pageStories = []
        #item[0]作者;item[1]内容;item[2]点赞数
        items = re.findall(pattern,pageCode)
        for item in items:
        #将item[1]内容中的换行符'<br/>'替换掉
            replaceBR = re.compile('<br/>')
            text = re.sub(replaceBR,'\n',item[1])
            #合并页面内容
            pageStories.append([item[0],text.strip(),item[2].strip()])
        return pageStories

    #加载并提取页面内容，加入到列表中
    def loadPage(self):
        #如果当前未看页数小于2，则加载
        if self.enable == True:
            if len(self.stories) < 2:
                pageStories = self.getPageItems(self.pageIndex)
                #将获取的新一页放入全局list中
                if pageStories:
                    self.stories.append(pageStories)
                    self.pageIndex += 1

    #每天回车键输出一个段子
    def getOneStoty(self,pageStories,page):
        for story in pageStories:
            input = raw_input().upper()
            self.loadPage()
            if input == "Q":
                self.enable = False
                return
            print u"第%d页\t作者：%s\t赞:%s\n%s" % (page,story[0],story[2],story[1])

    #开始方法
    def start(self):
        print u'正在读取糗事百科的内容，按回车查看新段子，Q退出'
        #使变量为True
        self.enable = True
        #加载一页内容
        self.loadPage()
        #局部变量，控制当前读到第几页
        nowPage = 0
        while self.enable:
            if len(self.stories) > 0:
                #从全局list中读取一页段子
                pageStories = self.stories[0]
                #当前读取页数
                nowPage += 1
                #删除全局list中第一个元素
                del self.stories[0]
                #输出该页段子
                self.getOneStoty(pageStories,nowPage)

spider = QSBK()
spider.start()
