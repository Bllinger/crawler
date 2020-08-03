# coding=UTF-8

import urllib2 as ul2
import urllib as ul
import cookielib as ckl
import re


def set_proxy(enable):
    if enable:
        proxy_handler = ul2.ProxyHandler({"http": "http://127.0.0.1:7890"})
        opener = ul2.build_opener(proxy_handler)
    else:
        null_proxy_handler = ul2.ProxyHandler({})
        opener = ul2.build_opener(null_proxy_handler)

    ul2.install_opener(opener)


if __name__ == '__main__':
    headers = {}
    content = ""  # type: str
    page = 1
    url = "https://www.qiushibaike.com/hot/page/" + str(page)
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"
    headers['User-Agent'] = user_agent

    try:
        request = ul2.Request(url, headers=headers)
        resp = ul2.urlopen(request)

        # print resp.read()
        content = resp.read().decode('utf-8')
        # name content imageLink agreeNum commentNum
        pattern = re.compile(r'<div.*?author clearfix">.*?<a.*?onclick.*?<h2.*?>(.*?)</h2>.*?' +
                             '<div.*?content">.*?<span.*?>(.*?)</span>.*?<!-- 图片或gif -->(.*?)<div.*?stats">.*?' +
                             '<span.*?stats-vote">.*?<i.*?number">(.*?)</i>.*?<span.*?stats-comments">.*?' +
                             '<i.*?number">(.*?)</i>', re.S)

        items = re.findall(pattern, content)
        for item in items:
            has_image = re.search(r'thumb">', item[2])
            if not has_image:
                print(item[0] + "\n" + item[1] + "\n" + item[3] + "\t" + item[4])


    except ul2.URLError, e:
        if hasattr(e, "code"):
            print e.code
        if hasattr(e, "reason"):
            print e.reason
    else:
        print "抓取成功"
