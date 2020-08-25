# coding=utf-8

import pickle
import time

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def login():
    browser = webdriver.Chrome()
    browser.get('https://m.weibo.cn/login?backURL=https://m.weibo.cn/')
    # time.sleep(120)
    # 创建显式等待对象
    wait = WebDriverWait(browser, 120)
    # 当出现登录输入框时则开始定位网页元素
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.input-wrapper')))
    user_name = browser.find_elements(By.CSS_SELECTOR, '#loginName')
    password = browser.find_elements(By.CSS_SELECTOR, '#loginPassword')
    btn = browser.find_elements(By.CSS_SELECTOR, '#loginAction')
    # 模拟输入用户名和密码并提交
    user_name.send_keys('your_username')
    password.send_keys('your_password')
    btn.click()
    # 当出现电话号码输入框时定位网页元素
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.m-btn_m-btn-block_m-btn-orange')))
    number = browser.find_elements(By.CSS_SELECTOR, '.fz16_fc-33_my-td-txt')
    btn_code = browser.find_elements(By.CSS_SELECTOR, '.m-btn_m-btn-block_m-btn-orange')
    # 模拟输入电话号码并提交
    number.send_keys('your_number')
    btn_code.click()
    # 当出现验证码输入框时定位网页元素
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.my-input_fz16_fc-33_my-td-txt')))
    code = browser.find_elements(By.CSS_SELECTOR, '.my-input_fz16_fc-33_my-td-txt')
    btn_submit = browser.find_elements(By.CSS_SELECTOR, '.m-btn_m-btn-block_m-btn-orange_m-btn-disabled')
    # 模拟输入验证码并提交
    code.send_keys(input("请输入验证码:"))
    btn_submit.click()

    return browser


def get_sina_cookies():
    with open('cookies.pickle', 'rb') as f:
        cookies = pickle.load(f)

    return cookies


def set_sina_cookies():
    browser = webdriver.Chrome()
    browser.get('https://m.weibo.cn/login?backURL=https://m.weibo.cn/')
    # time.sleep(120)
    wait = WebDriverWait(browser, 120)
    flag = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.weibo-text')))

    t = int(time.time())
    print time.strftime("%Y-%m-%d %H:%M:%S", to_local_time(t))
    cookies = browser.get_cookies()
    with open('cookies.pickle', 'wb') as f:
        pickle.dump(cookies, f)

    browser.quit()


def to_local_time(t):
    time_local = time.localtime(t)
    return time_local


def to_array_time(dt):
    time_array = time.strptime(dt, '%Y-%m-%d %H:%M:%S')
    time_stamp = time.mktime(time_array)
    return time_stamp


def add_cookies(cookies, browser):
    print "读取的cookie："
    for item in cookies:
        if item.has_key('expiry'):
            # print type(item['expiry'])
            time_local = to_local_time(item['expiry'])
            print item['name'] + '\t' + time.strftime("%Y-%m-%d %H:%M:%S", time_local)

    for item in cookies:
        if item.has_key('expiry'):
            if item['name'] == 'loginScene':
                print 'find loginScene'
                browser.add_cookie({
                    'domain': item['domain'],
                    'secure': item['secure'],
                    'value': item['value'],
                    'expiry': int(time.time()),
                    'path': item['path'],
                    'httpOnly': item['httpOnly'],
                    'name': item['name'],
                })
            elif item['name'] == '_T_WM':
                # item['expiry'] = int(time.time())
                delta = item['expiry'] - int(time.time())

                print "_T_WM失效的时间为：" + str(delta) + "s"
                if delta < 60:
                    expiry = int(time.time()) + 10 * 24 * 60 * 60
                    print '_T_WM：更新时间戳'
                else:
                    expiry = item['expiry']

                browser.add_cookie({
                    'domain': item['domain'],
                    'secure': item['secure'],
                    'value': item['value'],
                    'expiry': expiry,
                    'path': item['path'],
                    'httpOnly': item['httpOnly'],
                    'name': item['name'],
                })
            else:
                browser.add_cookie({
                    'domain': item['domain'],
                    'secure': item['secure'],
                    'value': item['value'],
                    'expiry': item['expiry'],
                    'path': item['path'],
                    'httpOnly': item['httpOnly'],
                    'name': item['name'],
                })
        else:
            browser.add_cookie({
                'domain': item['domain'],
                'secure': item['secure'],
                'value': item['value'],
                'path': item['path'],
                'httpOnly': item['httpOnly'],
                'name': item['name'],
            })


def sava_cookies(browser):
    cookies = browser.get_cookies()

    with open('cookies.pickle', 'wb') as f:
        pickle.dump(cookies, f)

    print "本次浏览所保存的cookie："
    for item in cookies:
        if item.has_key('expiry'):
            # print type(item['expiry'])
            time_local = to_local_time(item['expiry'])
            print item['name'] + '\t' + time.strftime("%Y-%m-%d %H:%M:%S", time_local)


def start():
    try:
        cookies = get_sina_cookies()
    except IOError, e:
        print e.message
        set_sina_cookies()
        cookies = get_sina_cookies()

    browser = webdriver.Chrome()
    browser.get('https://m.weibo.cn/profile/3944041983')
    add_cookies(cookies, browser)
    browser.get('https://m.weibo.cn/profile/3944041983')

    try:
        wait = WebDriverWait(browser, 60)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.weibo-text')))
    except TimeoutException, e:
        print '身份过期，需要重新登录，错误信息为：' + str(e.msg)
        set_sina_cookies()
        cookies = get_sina_cookies()
        browser.get('https://m.weibo.cn/profile/3944041983')
        add_cookies(cookies, browser)
        browser.get('https://m.weibo.cn/profile/3944041983')
        browser.close()

    browser.get('https://m.weibo.cn/profile/info?uid=3944041984')
    print browser.page_source
    sava_cookies(browser)
    browser.quit()
