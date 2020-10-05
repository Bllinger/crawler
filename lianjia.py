# coding=utf-8
import random
import sys
import pandas as pd
import numpy as np

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

import time
import pymysql
import requests
import re
from threading import Thread


def get_mysql_data(db):
    # db = pymysql.connect('localhost', 'root', '123456', 'lianjia', charset='utf8')

    try:
        cursor = db.cursor()
        sql = 'SELECT * FROM community_counts'
        cursor.execute(sql)
        results = cursor.fetchall()
    except Exception as e:
        print "error: " + str(e)
        results = None

    return results


def get_page(browser, url):
    browser.maximize_window()
    browser.get(url)
    wait = WebDriverWait(browser, 120)
    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.tabBox')))
    except:
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.tabBox')))
        except:
            pass

    return browser


def get_items_data(browser):
    temp_list = []
    items = browser.find_elements(By.CSS_SELECTOR, '.contentBox')
    try:
        for item in items:
            name = item.find_element(By.CSS_SELECTOR, 'div.itemContent > span.itemText.itemTitle').text
            distance = item.find_element(By.CSS_SELECTOR, 'div.itemContent > span.itemText.itemdistance').text
            note = item.find_element(By.CSS_SELECTOR, '.itemInfo').text

            record = name + '\t' + distance + '\t' + note
            # print record
            temp_list.append(record)
    except:
        temp_list[:] = []
        try:
            for item in items:
                name = item.find_element(By.CSS_SELECTOR, 'div.itemContent > span.itemText.itemTitle').text
                distance = item.find_element(By.CSS_SELECTOR, 'div.itemContent > span.itemText.itemdistance').text
                note = item.find_element(By.CSS_SELECTOR, '.itemInfo').text

                record = name + '\t' + distance + '\t' + note
                # print record
                temp_list.append(record)
        except:
            pass

    return temp_list


def switch_tag(browser, position):
    try:
        wait = WebDriverWait(browser, 120)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, position)))
    except:
        try:
            browser = switch_tag(browser, position)
        except:
            return browser

    temp_btn = browser.find_element(By.CSS_SELECTOR, position)
    browser.execute_script("arguments[0].scrollIntoView();", temp_btn)
    time.sleep(1)
    # temp_btn.click()
    webdriver.ActionChains(browser).move_to_element(temp_btn).click(temp_btn).perform()

    try:
        wait = WebDriverWait(browser, 5)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.itemContent > span.itemText.itemTitle')))
    except:
        pass

    return browser


def get_traffic_data(browser):
    subway_list = []
    bus_list = []
    print '获取交通数据'
    # 获取地铁数据
    time.sleep(3)
    subway_list = get_items_data(browser)
    print len(subway_list)
    # 切换到公交
    browser = switch_tag(browser, '#around > div > div.tabBox > div.itemTagBox > div:nth-child(2)')
    bus_list = get_items_data(browser)

    result_dic = {
        'subway': subway_list,
        'bus': bus_list
    }
    print '交通数据获取成功'
    print result_dic

    return result_dic


def get_school_data(browser):
    kindergarten_list = []
    primary_school_list = []
    secondary_school_list = []
    university_list = []

    print '获取教育数据'
    # 切换到教育
    browser = switch_tag(browser, '#around > div > div.tabBox > ul > li:nth-child(2)')
    # 获取幼儿园数据
    kindergarten_list = get_items_data(browser)

    # 点击小学
    temp_browser = switch_tag(browser, '#around > div > div.tabBox > div.itemTagBox > div:nth-child(2)')
    # 获取小学数据
    primary_school_list = get_items_data(temp_browser)

    # 点击中学
    temp_browser = switch_tag(browser, '#around > div > div.tabBox > div.itemTagBox > div:nth-child(3)')
    # 获取中学数据
    secondary_school_list = get_items_data(temp_browser)

    # 点击大学
    temp_browser = switch_tag(browser, '#around > div > div.tabBox > div.itemTagBox > div:nth-child(4)')
    # 获取大学数据
    university_list = get_items_data(temp_browser)

    result_dic = {
        'kindergarten': kindergarten_list,
        'primary_school': primary_school_list,
        'secondary_school': secondary_school_list,
        'university': university_list
    }

    print '获取教育数据成功'
    print result_dic

    return result_dic


def get_medical_data(browser):
    hospital_list = []
    pharmacy_list = []

    print '获取医疗数据'
    # 切换到医疗
    browser = switch_tag(browser, '#around > div > div.tabBox > ul > li:nth-child(3)')
    # 获取医院数据
    hospital_list = get_items_data(browser)
    # 切换到药店
    browser = switch_tag(browser, '#around > div > div.tabBox > div.itemTagBox > div:nth-child(2)')
    # 获取药店数据
    pharmacy_list = get_items_data(browser)

    result_dic = {
        'hospital': hospital_list,
        'pharmacy': pharmacy_list,
    }
    print '获取医疗数据成功'
    print result_dic
    return result_dic


def get_shopping_data(browser):
    mall_list = []
    supermarket_list = []
    market_list = []
    print '获取商圈数据'
    # 切换到购物
    browser = switch_tag(browser, '#around > div > div.tabBox > ul > li:nth-child(4)')
    # 获取商场数据
    mall_list = get_items_data(browser)
    # 切换到超市
    browser = switch_tag(browser, '#around > div > div.tabBox > div.itemTagBox > div:nth-child(2)')
    # 获取超市数据
    supermarket_list = get_items_data(browser)
    # 切换到市场
    browser = switch_tag(browser, '#around > div > div.tabBox > div.itemTagBox > div:nth-child(3)')
    # 获取市场数据
    market_list = get_items_data(browser)

    result_dic = {
        'mall': mall_list,
        'supermarket': supermarket_list,
        'market': market_list
    }
    print '获取商圈数据成功'
    print result_dic
    return result_dic


def get_life_data(browser):
    bank_list = []
    atm_list = []
    restaurant_list = []
    coffee_list = []

    print '获取生活数据'
    # 切换到生活
    browser = switch_tag(browser, '#around > div > div.tabBox > ul > li:nth-child(5)')
    # 获取银行数据
    bank_list = get_items_data(browser)
    # 切换到atm
    browser = switch_tag(browser, '#around > div > div.tabBox > div.itemTagBox > div:nth-child(2)')
    atm_list = get_items_data(browser)
    # 切换到餐厅
    browser = switch_tag(browser, '#around > div > div.tabBox > div.itemTagBox > div:nth-child(3)')
    restaurant_list = get_items_data(browser)
    # 切换到咖啡馆
    browser = switch_tag(browser, '#around > div > div.tabBox > div.itemTagBox > div:nth-child(4)')
    coffee_list = get_items_data(browser)

    result_dic = {
        'bank': bank_list,
        'atm': atm_list,
        'restaurant': restaurant_list,
        'coffee': coffee_list
    }
    print '获取生活数据成功'
    print result_dic
    return result_dic


def get_entertainment_data(browser):
    park_list = []
    cinema_list = []
    fitness_list = []
    gym_list = []
    print '获取娱乐数据'
    # 切换到娱乐
    browser = switch_tag(browser, '#around > div > div.tabBox > ul > li:nth-child(6)')
    # 获取公园数据
    park_list = get_items_data(browser)
    # 切换到电影院
    browser = switch_tag(browser, '#around > div > div.tabBox > div.itemTagBox > div:nth-child(2)')
    cinema_list = get_items_data(browser)
    # 切换到健身房
    browser = switch_tag(browser, '#around > div > div.tabBox > div.itemTagBox > div:nth-child(3)')
    fitness_list = get_items_data(browser)
    # 切换到体育馆
    browser = switch_tag(browser, '#around > div > div.tabBox > div.itemTagBox > div:nth-child(4)')
    gym_list = get_items_data(browser)

    result_dic = {
        'park': park_list,
        'cinema': cinema_list,
        'fitness': fitness_list,
        'gym': gym_list
    }
    print '娱乐数据获取成功'
    print result_dic
    return result_dic


def get_area_info(browser):
    # #dummybodyid > div.xiaoquDetailHeader > div > div.DetailFollow.fr > div > span
    wait = WebDriverWait(browser, 120)
    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.DetailFollow.fr > div > span')))
        print '成功找到'
        follow_number = browser.find_element(By.CSS_SELECTOR, 'div.DetailFollow.fr > div > span').text
        build_year = browser.find_element(By.CSS_SELECTOR,
                                          'div.xiaoquOverview > div.xiaoquDescribe.fr > div.xiaoquInfo > div:nth-child(1) > span.xiaoquInfoContent').text
        property_cost = browser.find_element(By.CSS_SELECTOR,
                                             'div.xiaoquOverview > div.xiaoquDescribe.fr > div.xiaoquInfo > div:nth-child(3) > span.xiaoquInfoContent').text
        property_lnc = browser.find_element(By.CSS_SELECTOR,
                                            'div.xiaoquOverview > div.xiaoquDescribe.fr > div.xiaoquInfo > div:nth-child(4) > span.xiaoquInfoContent').text
        build_lnc = browser.find_element(By.CSS_SELECTOR,
                                         'div.xiaoquOverview > div.xiaoquDescribe.fr > div.xiaoquInfo > div:nth-child(5) > span.xiaoquInfoContent').text
        building_num = browser.find_element(By.CSS_SELECTOR,
                                            'div.xiaoquOverview > div.xiaoquDescribe.fr > div.xiaoquInfo > div:nth-child(6) > span.xiaoquInfoContent').text
        room_num = browser.find_element(By.CSS_SELECTOR,
                                        'div.xiaoquOverview > div.xiaoquDescribe.fr > div.xiaoquInfo > div:nth-child(7) > span.xiaoquInfoContent').text

        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#frameDeal > a')))
            sell_link = browser.find_element(By.CSS_SELECTOR, '#frameDeal > a').get_attribute('href')
        except:
            try:
                sell_link = browser.find_element(By.CSS_SELECTOR, '#frameDeal > a').get_attribute('href')
            except:
                sell_link = ''
    except:
        pass


    result_dic = {
        'follow_number': follow_number,
        'build_year': build_year,
        'property_cost': property_cost,
        'property_lnc': property_lnc,
        'build_lnc': build_lnc,
        'building_num': building_num,
        'room_num': room_num,
        'sell_link': sell_link
    }
    print '获取小区信息成功'
    print result_dic
    return result_dic


def save_in_mysql(db, name, traffic_dic, school_dic, medical_dic, shopping_dic, life_dic, entertainment_dic, area_info_dic):
    print '开始保存至数据库'
    subways = "\\".join(traffic_dic['subway'])  # str(traffic_dic['subway'])
    bus = "\\".join(traffic_dic['bus'])

    kindergarten = "\\".join(school_dic['kindergarten'])
    primary_school = "\\".join(school_dic['primary_school'])
    secondary_school = "\\".join(school_dic['secondary_school'])
    university = "\\".join(school_dic['university'])

    hospital = "\\".join(medical_dic['hospital'])
    pharmacy = "\\".join(medical_dic['pharmacy'])

    mall = "\\".join(shopping_dic['mall'])
    supermarket = "\\".join(shopping_dic['supermarket'])
    market = "\\".join(shopping_dic['market'])

    bank = "\\".join(life_dic['bank'])
    atm = "\\".join(life_dic['atm'])
    restaurant = "\\".join(life_dic['restaurant'])
    coffee = "\\".join(life_dic['coffee'])

    park = "\\".join(entertainment_dic['park'])
    cinema = "\\".join(entertainment_dic['cinema'])
    fitness = "\\".join(entertainment_dic['fitness'])
    gym = "\\".join(entertainment_dic['gym'])

    follow_number = area_info_dic['follow_number']
    build_year = area_info_dic['build_year']
    property_cost = area_info_dic['property_cost']
    property_lnc = area_info_dic['property_lnc']
    build_lnc = area_info_dic['build_lnc']
    building_num = area_info_dic['building_num']
    room_num = area_info_dic['room_num']
    sell_link = area_info_dic['sell_link']

    try:
        db.ping(reconnect=True)
    except:
        db = pymysql.connect('localhost', 'root', '123456', 'lianjia', charset='utf8', connect_timeout=24 * 60 * 60)

    try:
        cursor = db.cursor()
        sql = 'INSERT INTO around_data(name,subways,bus,kindergarten,primary_school,secondary_school,university,hospital,pharmacy,mall,supermarket,market,bank,atm,restaurant,coffee,park,cinema,fitness,gym,follow_number,build_year,property_cost,property_lnc,build_lnc,building_num,room_num,sell_link) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        cursor.execute(sql, (name, subways, bus, kindergarten, primary_school, secondary_school,
                             university, hospital, pharmacy, mall, supermarket, market, bank, atm, restaurant, coffee,
                             park, cinema, fitness, gym,follow_number,build_year,property_cost,property_lnc,build_lnc,building_num,room_num,sell_link))
        print cursor.lastrowid
        db.commit()
    except Exception as e:
        print "error: " + str(e)
        db.rollback()


def test_proxy(ip):
    print '测试: ' + ip
    proxy = {
        "http": ip
    }
    try:
        resp = requests.get('http://httpbin.org/get', proxies=proxy, timeout=1000)
        print 'ip为：' + resp.text
        if resp.status_code == 200:
           print ip
           return True
        else:
            return False
    except Exception ,e:
        return False


def get_browser(ips):
    ip = ''
    for _ in range(0, len(ips)):
        index = random.randint(0, len(ips)-1)
        if test_proxy(ips[index]):
            ip = ips[index]
            break

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--proxy-server=http://%s' % ip)
    browser = webdriver.Chrome(chrome_options=chrome_options)
    # browser.get('http://httpbin.org/ip')
    #
    # print browser.page_source

    return browser


def start(start, end, results, db):
    reload(sys)
    sys.setdefaultencoding('utf-8')
    #
    # f = open('/Users/blinger/Downloads/proxy.txt')
    # lines = f.readlines()
    # ips = []
    # for line in lines:
    #     line = re.sub('\r\n', '', line)
    #     ips.append(line)
    # print 'ip池装载成功'

    traffic_dic = {}
    school_dic = {}
    medical_dic = {}
    shopping_dic = {}
    life_dic = {}
    entertainment_dic = {}

    chrome_options = webdriver.ChromeOptions()  # 建一个参数对象，用来控制chrome以无界面模式打开
    chrome_options.add_argument('--no-sandbox')  # 取消沙盒模式,浏览器的安全性会降低，如果不取消,linux下运行会报错
    chrome_options.add_argument('--headless')  # 浏览器不提供可视化页面
    chrome_options.add_argument('--disable-gpu')  # 禁用GPU加速

    browser = webdriver.Chrome()  # chrome_options=chrome_options

    results = results[start-1:end]
    for item in results:
        name = item[1].decode('utf-8')
        url = item[2].decode('utf-8')

        # browser = get_browser(ips) # 切换代理
        browser = get_page(browser, url)
        list_page_handle = browser.current_window_handle
        area_info_dic = get_area_info(browser)
        traffic_dic = get_traffic_data(browser)
        school_dic = get_school_data(browser)
        medical_dic = get_medical_data(browser)
        shopping_dic = get_shopping_data(browser)
        life_dic = get_life_data(browser)
        entertainment_dic = get_entertainment_data(browser)

        save_in_mysql(db, name, traffic_dic, school_dic, medical_dic, shopping_dic, life_dic, entertainment_dic, area_info_dic)
        # browser.close()
        #browser.quit()

    # browser.get("https://cq.lianjia.com/xiaoqu/3611060982243/")
    #
    # time.sleep(10)
    # browser.close()
    # browser.switch_to.window(list_page_handle)


db = pymysql.connect('localhost', 'root', '123456', 'lianjia', charset='utf8', connect_timeout=24*60*60)
def init():
    df = pd.read_csv('/Users/blinger/Downloads/house_info.csv', header=None, names=['id', 'position', 'name', 'url'])
    temp_df = df[df['position'] == 'jiangbei'][['id', 'name', 'url']]
    results = np.array(temp_df).tolist()
    # db = pymysql.connect('localhost', 'root', '123456', 'lianjia', charset='utf8', connect_timeout=24 * 60 * 60)
    results = get_mysql_data(db)

    thread_list = []
    t1 = Thread(target=start, args=(1, 1, results, db))
    t1.start()
    t2 = Thread(target=start, args=(2, 2, results, db))
    t2.start()
    t3 = Thread(target=start, args=(3, 3, results, db))
    t3.start()
    t4 = Thread(target=start, args=(4, 4, results, db))
    t4.start()
    t5 = Thread(target=start, args=(5, 5, results, db))
    t5.start()
    t6 = Thread(target=start, args=(6, 6, results, db))
    t6.start()
    t7 = Thread(target=start, args=(7, 7, results, db))
    t7.start()
    t8 = Thread(target=start, args=(8, 8, results, db))
    t8.start()
    t9 = Thread(target=start, args=(9, 9, results, db))
    t9.start()

    thread_list.append(t1)
    thread_list.append(t2)
    thread_list.append(t3)
    thread_list.append(t4)
    thread_list.append(t5)
    thread_list.append(t6)
    thread_list.append(t7)
    thread_list.append(t8)
    thread_list.append(t9)

    for t in thread_list:
        t.join()

    db.close()

