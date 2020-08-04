# coding=utf-8

import urllib2
import re


# 传入某一页的索引获得页面的html代码
def get_page(self, page_index):
    try:
        url = self.url + str(page_index)

        request = urllib2.Request(url, headers=self.headers)
        resp = urllib2.urlopen(request)
        page_code = resp.read().decode('utf-8')

    except urllib2.URLError, e:
        if hasattr(e, 'code'):
            print e.code
        if hasattr(e, 'reason'):
            print e.reason
        return None

    else:
        print "抓取页面成功"
        return page_code


# 传入某一页代码，调用get_page函数
# 得到html代码后进行正则匹配获取内容，并返回段子列表
def get_page_item(self, page_index):
    page_code = self.get_page(self, page_index)

    pattern = re.compile('<div.*?author clearfix">.*?<a.*?onclick.*?<h2.*?>(.*?)</h2>.*?' +
                         '<div.*?content">.*?<span.*?>(.*?)</span>(.*?)' +
                         '<div.*?stats">.*?<span.*?stats-vote">.*?number">(.*?)</i>.*?' +
                         '<span.*?stats-comments">.*?<i.*?number">(.*?)</i>', re.S)
    items = re.findall(pattern, page_code)
    page_stores = []

    # print "items的大小为: " + str(len(items))
    for item in items:
        have_imag = re.search('thumb">', item[2])
        if not have_imag:
            text = re.sub('<br/>', '\n', item[1])
            page_stores.append([item[0].strip(), text.strip(), item[3].strip(), item[4].strip()])
            # print str(len(page_stores)) + "\t" + item[0]

    print "<-------------------------开始阅读" + str(page_index) + "页------------------------->"
    return page_stores


def start(self):
    print "<--------------按回车开始抓取糗事百科，输入Q结束爬取-------------->"
    # 初始化页面索引
    self.page_index = 1
    self.user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
    # 添加header，绕过服务器的header验证
    self.headers = {'User-Agent': self.user_agent}
    # 初始化段子列表
    self.stories = []
    self.enable = False
    self.url = 'https://www.qiushibaike.com/hot/page/'

    input = raw_input()
    if input == "Q":
        self.enable = False
        print "<---------------------------程序结束--------------------------->"
        return
    self.enable = True
    # 初始化段子列表索引
    item_index = 0
    while self.enable:
        if item_index > len(self.stories) - 1:
            # 获取段子内容
            self.stories = self.get_page_item(self, self.page_index)
            self.page_index += 1
            item_index = 0
            print "共有" + str(len(self.stories)) + "则故事"
            print "<-------------------------按回车开始阅读------------------------->"

        input = raw_input()
        if input == "Q":
            self.enable = False

        story = self.stories[item_index]
        item_index += 1
        print "作者：" + story[0] + "\n" + story[1] + "\n点赞数：" + story[2] + "\t评论数：" + story[3]

    print "<---------------------------程序结束--------------------------->"