# coding=utf-8

import urllib2 as ul2
import urllib as ul
import cookielib as ckl
import re
import qsbk
import sina
import lianjia
import requests
from bs4 import BeautifulSoup
import lxml
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pickle
import sys
import time
import datetime

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


def get_sina_cookies():
    with open('cookies.pickle', 'rb') as f:
        cookies = pickle.load(f)

    return cookies


def set_sina_cookies():
    browser = webdriver.Chrome()
    browser.get('https://m.weibo.cn/login?backURL=https://m.weibo.cn/')
    #time.sleep(120)
    wait = WebDriverWait(browser, 120)
    flag = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.weibo-text')))

    cookies = browser.get_cookies()
    with open('cookies.pickle', 'wb') as f:
        pickle.dump(cookies, f)

    browser.close()


def to_local_time(t):
    time_local = time.localtime(t)
    return time_local


def to_array_time(dt):
    time_array = time.strptime(dt, '%Y-%m-%d %H:%M:%S')
    time_stamp = time.mktime(time_array)
    return time_stamp


if __name__ == '__main__':
    lianjia.init()
    #lianjia.start()
    #set_sina_cookies()
    # cookies = get_sina_cookies()
    # print cookies
    # # for item in cookies:
    # #     print 'domain: ' + str(item['domain'])
    # #     print 'secure: ' + str(item['secure'])
    # #     print 'value: ' + str(item['value'])
    # #     print 'path: ' + str(item['path'])
    # #     print 'httpOnly: ' + str(item['httpOnly'])
    # #     print 'name: ' + str(item['name'])
    # #     if item.has_key('expiry'):
    # #         print 'expiry: ' + str(item['expiry'])
    # #     else:
    # #         print 'none'
    # #     print
    # #     print
    # print "浏览前的cookie："
    # for item in cookies:
    #     if item.has_key('expiry'):
    #         # print type(item['expiry'])
    #         time_local = to_local_time(item['expiry'])
    #         print item['name'] + '\t' + time.strftime("%Y-%m-%d %H:%M:%S", time_local)
    #
    # browser = webdriver.Chrome()
    # browser.get('https://m.weibo.cn/')
    #
    # for item in cookies:
    #     if item.has_key('expiry'):
    #         if item['name'] == 'loginScene':
    #             print 'find loginScene'
    #             browser.add_cookie({
    #                 'domain': item['domain'],
    #                 'secure': item['secure'],
    #                 'value': item['value'],
    #                 'expiry': item['expiry'],  #int(time.time()),
    #                 'path': item['path'],
    #                 'httpOnly': item['httpOnly'],
    #                 'name': item['name'],
    #             })
    #         elif item['name'] == '_T_WM':
    #             #item['expiry'] = int(time.time())
    #             delta = item['expiry'] - int(time.time())
    #
    #             print "时间差为：" + str(delta) + "s"
    #             if delta < 60:
    #                 expiry = int(time.time()) + 10*24*60*60
    #                 print '_T_WM：更新时间戳'
    #             else:
    #                 expiry = item['expiry']
    #
    #             #expiry = item['expiry']
    #             browser.add_cookie({
    #                 'domain': item['domain'],
    #                 'secure': item['secure'],
    #                 'value': item['value'],
    #                 'expiry': expiry,
    #                 'path': item['path'],
    #                 'httpOnly': item['httpOnly'],
    #                 'name': item['name'],
    #             })
    #         else:
    #             browser.add_cookie({
    #                 'domain': item['domain'],
    #                 'secure': item['secure'],
    #                 'value': item['value'],
    #                 'expiry': item['expiry'],
    #                 'path': item['path'],
    #                 'httpOnly': item['httpOnly'],
    #                 'name': item['name'],
    #             })
    #     else:
    #         browser.add_cookie({
    #             'domain': item['domain'],
    #             'secure': item['secure'],
    #             'value': item['value'],
    #             'path': item['path'],
    #             'httpOnly': item['httpOnly'],
    #             'name': item['name'],
    #         })
    #
    # browser.get('https://m.weibo.cn/')
    # # with open('cookies.pickle','rb') as f:
    # #     print pickle.load(f)
    # wait = WebDriverWait(browser,120)
    # flag = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.weibo-text')))
    # #print(browser.page_source)
    #
    # cookies = browser.get_cookies()
    #
    # with open('cookies.pickle', 'wb') as f:
    #     pickle.dump(cookies, f)
    #
    # print "浏览后的cookie："
    # for item in cookies:
    #     if item.has_key('expiry'):
    #         # print type(item['expiry'])
    #         time_local = to_local_time(item['expiry'])
    #         print item['name'] + '\t' + time.strftime("%Y-%m-%d %H:%M:%S", time_local)
    #
    # time.sleep(10)
    # browser.quit()

    #
    # cookies = browser.get_cookies()
    #
    # print browser.page_source
    #


    # session = requests.Session()
    #
    # headers = {
    #
    # }
    # i = "1"
    #
    # print type(int(i))
    # ## 糗事百科
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
