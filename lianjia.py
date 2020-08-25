# coding=utf-8

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


def get_page(browser,url):
    url = "https://cq.lianjia.com/xiaoqu/3611060982243/"
    browser.get(url)
    wait = WebDriverWait(browser, 120)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.contentBox')))

    print browser.page_source
    return browser


def get_traffic_data(browser):
    subway_list = []
    bus_list = []

    #print browser.page_source

    subway_items = browser.find_elements(By.CSS_SELECTOR, '.contentBox')
    for item in subway_items:
        # #mapListContainer > ul > li:nth-child(1) > div > div.itemContent > span.itemText.itemTitle
        station = item.find_element(By.CSS_SELECTOR, 'div.itemContent > span.itemText.itemTitle').text
        distance = item.find_element(By.CSS_SELECTOR, 'div.itemContent > span.itemText.itemdistance').text
        paths = item.find_element(By.CSS_SELECTOR, '.itemInfo').text

        subway_dic = {
            'station': station,
            'distance': distance,
            'paths': paths
            }
        subway_list.append(subway_dic)

    #around > div > div.tabBox > div.itemTagBox > div:nth-child(2)
    time.sleep(3)
    bus_btn = browser.find_element(By.CSS_SELECTOR, '#around > div > div.tabBox > div.itemTagBox > div:nth-child(2)')
    # 让切换按钮滚动可见
    browser.execute_script("arguments[0].scrollIntoView();", bus_btn)
    time.sleep(3)
    webdriver.ActionChains(browser).move_to_element(bus_btn).click(bus_btn).perform()
    time.sleep(3)

    bus_items = browser.find_elements(By.CSS_SELECTOR, '.contentBox')
    for item in bus_items:
        station = item.find_element(By.CSS_SELECTOR, 'div.itemContent > span.itemText.itemTitle').text
        distance = item.find_element(By.CSS_SELECTOR, 'div.itemContent > span.itemText.itemdistance').text
        paths = item.find_element(By.CSS_SELECTOR, '.itemInfo').text

        bus_dic = {
            'station': station,
            'distance': distance,
            'paths': paths
        }
        bus_list.append(bus_dic)

    print bus_list


def start():
    db = pymysql.connect('localhost', 'root', '123456', 'lianjia', charset='utf8')

    chrome_options = Options()
    # 设置chrome浏览器无界面模式
    chrome_options.add_argument('--headless')
    browser = webdriver.Chrome() #chrome_options=chrome_options

    # results = get_mysql_data(db)
    # for item in results:
    #     print item[1].decode('utf-8') + '\t' + item[2].decode('utf-8')
    #     url = item[2].decode('utf-8')
        #get_page(browser, url)

    browser = get_page(browser, url=None)
    get_traffic_data(browser)

    # browser.get("https://cq.lianjia.com/xiaoqu/3611060982243/")
    #
    time.sleep(120)
    browser.quit()
    db.close()