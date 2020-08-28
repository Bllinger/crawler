# coding=utf-8
import sys

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

import time
import pymysql


def get_mysql_data(db):
    #db = pymysql.connect('localhost', 'root', '123456', 'lianjia', charset='utf8')

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
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.tabBox')))

    #print browser.page_source
    return browser


def get_items_data(browser):
    temp_list = []
    items = browser.find_elements(By.CSS_SELECTOR, '.contentBox')
    for item in items:
        name = item.find_element(By.CSS_SELECTOR, 'div.itemContent > span.itemText.itemTitle').text
        distance = item.find_element(By.CSS_SELECTOR, 'div.itemContent > span.itemText.itemdistance').text
        note = item.find_element(By.CSS_SELECTOR, '.itemInfo').text

        record = name+'\t'+distance+'\t'+note
        #print record
        temp_list.append(record)

    return temp_list


def switch_tag(browser, position):
    temp_btn = browser.find_element(By.CSS_SELECTOR, position)
    browser.execute_script("arguments[0].scrollIntoView();", temp_btn)
    time.sleep(3)
    #temp_btn.click()
    webdriver.ActionChains(browser).move_to_element(temp_btn).click(temp_btn).perform()
    time.sleep(3)
    return browser


def get_traffic_data(browser):
    subway_list = []
    bus_list = []
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
    return result_dic


def get_school_data(browser):
    kindergarten_list = []
    primary_school_list = []
    secondary_school_list = []
    university_list = []

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
    return result_dic


def get_medical_data(browser):
    hospital_list = []
    pharmacy_list = []

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
    return result_dic


def get_shopping_data(browser):
    mall_list = []
    supermarket_list = []
    market_list = []

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
    return result_dic


def get_life_data(browser):
    bank_list = []
    atm_list = []
    restaurant_list = []
    coffee_list = []

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
    return result_dic


def get_entertainment_data(browser):
    park_list = []
    cinema_list = []
    fitness_list = []
    gym_list = []

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
    return result_dic


def save_in_mysql(db, name, traffic_dic, school_dic, medical_dic, shopping_dic, life_dic, entertainment_dic):
    subways = "\\".join(traffic_dic['subway'])#str(traffic_dic['subway'])
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

    try:
        cursor = db.cursor()
        sql = 'INSERT INTO around_data(name,subways,bus,kindergarten,primary_school,secondary_school,university,hospital,pharmacy,mall,supermarket,market,bank,atm,restaurant,coffee,park,cinema,fitness,gym) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        cursor.execute(sql,(name,subways,bus,kindergarten,primary_school,secondary_school,
              university,hospital,pharmacy,mall,supermarket,market,bank,atm,restaurant,coffee,
              park,cinema,fitness,gym))
        print cursor.lastrowid
        db.commit()
    except Exception as e:
        print "error: " + str(e)
        db.rollback()


def start():
    reload(sys)
    sys.setdefaultencoding('utf-8')

    db = pymysql.connect('localhost', 'root', '123456', 'lianjia', charset='utf8')
    traffic_dic = {}
    school_dic = {}
    medical_dic = {}
    shopping_dic = {}
    life_dic = {}
    entertainment_dic = {}

    chrome_options = Options()
    # 设置chrome浏览器无界面模式
    chrome_options.add_argument('--headless')
    browser = webdriver.Chrome() #chrome_options=chrome_options

    results = get_mysql_data(db)
    results = results[23:]
    for item in results:
        name = item[1].decode('utf-8')
        url = item[2].decode('utf-8')

        browser = get_page(browser, url)
        traffic_dic = get_traffic_data(browser)
        school_dic = get_school_data(browser)
        medical_dic = get_medical_data(browser)
        shopping_dic = get_shopping_data(browser)
        life_dic = get_life_data(browser)
        entertainment_dic = get_entertainment_data(browser)

        save_in_mysql(db,name,traffic_dic,school_dic,medical_dic,shopping_dic,life_dic,entertainment_dic)
        #browser.close()

    # browser.get("https://cq.lianjia.com/xiaoqu/3611060982243/")
    #
    time.sleep(10)
    browser.quit()
    db.close()