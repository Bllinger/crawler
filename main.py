# coding=utf-8

import urllib2 as ul2
import urllib as ul
import cookielib as ckl
import re
import qsbk

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
    qsbk.start(self=qsbk)
