# coding=utf-8

import asyncio
from pathlib import Path
from sys import path



import pymysql
from pyquery import PyQuery as pq

async def screen_size():
    """使用tkinter获取屏幕大小"""
    import tkinter
    tk = tkinter.Tk()
    width = tk.winfo_screenwidth()
    height = tk.winfo_screenheight()
    tk.quit()
    return width, height


async def save_in_mysql(db, name, profile_link, fans_count, work_count, completion_rate, organization, image_url, grade, domain):
    try:
        cursor = db.cursor()
        sql = 'INSERT INTO taobaomm(name, profile_link, fans_count, work_count, completion_rate, organization, image_url, grade, domain) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)'
        cursor.execute(sql, (name, profile_link, fans_count, work_count, completion_rate, organization, image_url, grade, domain))
        print(cursor.lastrowid)
        db.commit()
    except Exception as e:
        print("error: " + str(e))
        db.rollback()


async def get_data(db, page):
    total_page = int(
        (await (await (await page.J('span.next-pagination-display')).getProperty('textContent')).jsonValue()).split(
            '/')[1])
    print("总页数：" + str(total_page))
    print(type(total_page))

    now_page = 1
    while now_page <= total_page:
        while not await page.J('.anchor-profile-info'):
            pass

        links = await page.JJ('.anchor-card')
        print("links的大小为：" + str(len(links)))

        for item in links:
            print('进入第' + str(now_page) + '页')
            name = await (await (await (item.J('div.anchor-info-body > h3'))).getProperty('textContent')).jsonValue()
            link = await (await (await (item.J('a.anchor-profile-info'))).getProperty('href')).jsonValue()
            fans_count = await (await (await (item.J('span.fans-count'))).getProperty('textContent')).jsonValue()

            work_count = await (
                await (await (item.J('ul.anchor-base-info > li:nth-child(1) > span.info-item-value'))).getProperty(
                    'textContent')).jsonValue()
            grade = await (
                await (await (item.J('ul.anchor-base-info > li:nth-child(2) > span.info-item-value'))).getProperty(
                    'textContent')).jsonValue()
            completion_rate = await (
                await (await (item.J('ul.anchor-base-info > li:nth-child(3) > span.info-item-value'))).getProperty(
                    'textContent')).jsonValue()
            domain = await (
                await (await (item.J('ul.anchor-base-info > li:nth-child(4) > span.info-item-value'))).getProperty(
                    'textContent')).jsonValue()
            try:
                organization = await (
                    await (await (item.J('ul.anchor-base-info > li:nth-child(5) > span.info-item-value'))).getProperty(
                        'textContent')).jsonValue()
            except AttributeError as e:
                print("error: " + str(e))
                organization = '个人'

            image_url = await (
                await (await (item.J('div.ice-img.sharp.anchor-avatar > img'))).getProperty('src')).jsonValue()

            print(str(name) + '\t' + str(link) + '\t' + str(
                fans_count) + '\t' + work_count + '\t' + grade + '\t' + completion_rate + '\t' + organization + '\t' + grade + '\t' + domain)
            # await save_in_mysql(db, name, link, fans_count, work_count, completion_rate, organization, image_url, grade, domain)

        await asyncio.sleep(30)
        now_page += 1
        if now_page <= total_page:
            while not await page.J('.next-btn.next-btn-normal.next-btn-medium.next-pagination-item.next'):
                pass
            await page.click('.next-btn.next-btn-normal.next-btn-medium.next-pagination-item.next')


async def main():
    db = pymysql.connect('localhost', 'root', '123456', 'taobao', charset='utf8')
    # executablePath='C:\\Users\\Administrator\\AppData\\Local\\Google\\Chrome\\Application\\chrome.exe',
    p = Path("./myUserDataDir")
    p1 = Path("./temp")

    print("打开浏览器")
    browser = await launch(
                           #executablePath='C:\\Users\\Administrator\\AppData\\Local\\Google\\Chrome\\Application\\chrome.exe',
                           headless=False,
                           userDataDir=p1.resolve(), # "F:\\python\\crawler\\temp",
                           args=[
                                 "--disable-infobars",
                                 '--start-maximized',
                                 #"--user-data-dir=./myUserDataDir",
                                 #"--load-extension=./runningJS/",
                                 #"--disable-extensions-except=./runningJS/",
                                 ])
    print("打开网页")
    page = await browser.newPage()
    # await page.setUserAgent(
    #     'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36')
    print("执行脚本")
    await page.evaluateOnNewDocument('''() => {
            Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
            })
            }
        ''')

    width, height = await screen_size()
    print(str(width) + '\t' + str(height))
    await page.setViewport({'width': width, 'height': height})
    await page.goto('https://v.taobao.com/v/content/live?catetype=704')
    # await page.goto('https://www.taobao.com')

    print("开始访问")
    # resp = await page.goto('https://www.weibo.com')
    await asyncio.sleep(3)
    print("开始截图")
    # #print(await page.title())
    await page.screenshot(path="2.png", fullPage=False)
    print("截图成功2")
    while not await page.waitForSelector('.WB_feed_handle', timeout=300000):
        pass
    # while not await page.waitForSelector('.anchor-card-content', timeout=300000):
    #     pass
    print("页面加载成功")
    await page.screenshot(path="1.png", fullPage=False)
    print("截图成功")
    print(pq(await page.content()))
    #await get_data(db, page)

    await asyncio.sleep(10)
    await page.close()
    await browser.close()


asyncio.get_event_loop().run_until_complete(main())
