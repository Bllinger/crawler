# coding=utf-8

import urllib2 as ul2
import urllib as ul
import cookielib as ckl
import re
import qsbk
import requests
from bs4 import BeautifulSoup
import lxml

import sys

reload(sys)

sys.setdefaultencoding('utf-8')


def set_proxy(enable):
    if enable:
        proxy_handler = ul2.ProxyHandler({"http": "http://127.0.0.1:7890"})
        opener = ul2.build_opener(proxy_handler)
    else:
        null_proxy_handler = ul2.ProxyHandler({})
        opener = ul2.build_opener(null_proxy_handler)

    ul2.install_opener(opener)


if __name__ == '__main__':
    # session = requests.Session()
    #
    # headers = {
    #
    # }
    url = 'https://www.zhihu.com'
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
    # 添加header，绕过服务器的header验证
    headers = {'User-Agent': user_agent}
    resp = requests.get(url, headers=headers)

    print resp.text
    ## 糗事百科
    # user_id = []
    # content = []
    # image = []
    # enjoy_num = []
    # comment_num = []
    #
    # user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
    # # 添加header，绕过服务器的header验证
    # headers = {'User-Agent': user_agent}
    # resp = requests.get("https://www.qiushibaike.com/hot/page/1", headers=headers)
    #
    # soup = BeautifulSoup(resp.text, 'lxml')
    # user_id_items = soup.find_all('a', onclick="_hmt.push(['_trackEvent','web-list-author-text','chick'])")
    # content_items = soup.find_all('div', class_='content')
    # enjoy_num_items = soup.find_all('span', class_='stats-vote')
    # comment_num_items = soup.find_all('span', class_='stats-comments')
    #
    # for item in user_id_items:
    #     user_id.append(item.contents[1].string.strip())
    #
    # for item in content_items:
    #     string = ''
    #     for s in item.strings:
    #         if s != '\n':
    #             string += s.strip()
    #             #content.append(s.strip())
    #     content.append(string)
    #
    # for item in enjoy_num_items:
    #     enjoy_num.append(item.i.string)
    #
    # for item in comment_num_items:
    #     comment_num.append(item.a.i.string)
    #
    # i = 0
    # while i <= len(user_id)-1:
    #     print "用户id：" + user_id[i]
    #     print content[i]
    #     print "点赞数为：" + enjoy_num[i] + "\t评论数为：" + comment_num[i]
    #     print ''
    #     i += 1
    #qsbk.start(self=qsbk)
