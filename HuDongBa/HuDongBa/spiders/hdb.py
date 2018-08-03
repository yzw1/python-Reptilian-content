# -*- coding: utf-8 -*-
import scrapy
import time
import redis
import re
import os
import datetime
import traceback
from lxml import etree
from HuDongBa.items import HudongbaItem
from HuDongBa import settings
from bs4 import BeautifulSoup
import js2xml
import pymysql
import pymysql.cursors

class HdbSpider(scrapy.Spider):
    name = 'hdb'
    allowed_domains = ['http://www.hdb.com/']
    start_urls = ['http://www.hdb.com/']
    #全国
    globalUrl = ['http://www.hdb.com/quanguo/']

    def start_requests(self):
        # print(sys.path)
        url = self.globalUrl[0]
        print(url)
        yield scrapy.Request(url,self.process_Parse)

    def process_Parse(self,response):
        result = redis.Redis(host='localhost', port=6379, decode_responses=True)
        be = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        result.set('hbe', be)
        #log
        MYSQL_HOSTS = settings.MYSQL_HOSTS
        MYSQL_USER = settings.MYSQL_USER
        MYSQL_PASSWORD = settings.MYSQL_PASSWORD
        MYSQL_PORT = settings.MYSQL_PORT
        MYSQL_DB = settings.MYSQL_DB

        config = {
            'user': MYSQL_USER,
            'password': MYSQL_PASSWORD,
            'host': MYSQL_HOSTS,
            'db': MYSQL_DB,
            'port': MYSQL_PORT,
            'charset': 'utf8mb4',
            'cursorclass': pymysql.cursors.DictCursor,
        }
        cnx = pymysql.connect(**config)
        cur = cnx.cursor()

        name = 'hdb'
        StartTime = result.get('hbe')
        EndTime = result.get('hen')
        RecordNum = result.get('hnum')
        error = result.get('herror')
        if (error):
            Error = error
        else:
            Error = ''
        CrawlerStatus = 0
        sql = "INSERT INTO CrawlerLog (`name`,StartTime,EndTime,RecordNum,CrawlerStatus,Error) VALUES (%s, %s, %s, %s, %s, %s)"
        print(sql)
        ret = cur.execute(sql, (name, StartTime, EndTime, RecordNum, CrawlerStatus, Error))
        sqls = 'select max(id) as id from CrawlerLog;'
        rets = cur.execute(sqls)
        # 获取最后的数量
        rs = cur.fetchall()
        for r in rs:
            print(r['id'])
            result.set('hid', r['id'])

        sq = "select count(1) as das from HuDongBa"
        cur.execute(sq)
        rss = cur.fetchall()
        for r in rss:
            print(r['das'])
            result.set('hdas', r['das'])
        cnx.commit()


        # python Reptilian content
        end = result.get('page')
        if (end):
            end = result.get('page')
        else:
            end = 0
        first = int(end) + 1
        url = response.url
        #get message
        resp = bytes(bytearray(response.text, encoding='utf-8'))
        html = etree.HTML(resp)
        #获取类别属性值
        dates = html.xpath("//li[@class = 'header_nav_li']")
        num = '-0-2-0-0-'

        for pages in range(first,125):
            page = str(pages)
            for data in dates:
                ti = data.xpath(".//@id")[0]
                print(ti)
                kind = url + ti + num
                urls = kind + page
                result.set('page', page)
                print(urls)
                try:
                    yield scrapy.Request(urls,self.parse,dont_filter=True)
                    time.sleep(3)
                except Exception as e:
                    # error = logging.exception('error')
                    s = traceback.extract_tb(sys.exc_info()[2])
                    result.set('hesss', s)
                    result.set('hess', e)

                    MYSQL_HOSTS = settings.MYSQL_HOSTS
                    MYSQL_USER = settings.MYSQL_USER
                    MYSQL_PASSWORD = settings.MYSQL_PASSWORD
                    MYSQL_PORT = settings.MYSQL_PORT
                    MYSQL_DB = settings.MYSQL_DB

                    config = {
                        'user': MYSQL_USER,
                        'password': MYSQL_PASSWORD,
                        'host': MYSQL_HOSTS,
                        'db': MYSQL_DB,
                        'port': MYSQL_PORT,
                        'charset': 'utf8mb4',
                        'cursorclass': pymysql.cursors.DictCursor,
                    }
                    cnx = pymysql.connect(**config)
                    cur = cnx.cursor()
                    Wlocal = result.get('hesss')
                    print(Wlocal)
                    WebpageError = result.get('hess')
                    print(WebpageError)
                    CrawlerStatus = 1
                    print(CrawlerStatus)
                    RecordNum = 0
                    print(RecordNum)
                    id = result.get('hid')
                    print(id)
                    EndTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    print(EndTime)
                    date = cur.execute(
                        'UPDATE CrawlerLog SET RecordNum = %s,WebpageError = %s,CrawlerStatus= %s,EndTime = %s,Wlocal = %s WHERE id = %s',
                        (RecordNum, WebpageError, CrawlerStatus, EndTime, Wlocal, id))
                    print(date)
                    cnx.commit()
    #msg
    def parse(self, response):
        result = redis.Redis(host='localhost', port=6379, decode_responses=True)
        resp = response.text
        # print(resp)
        html = etree.HTML(resp)
        # 获取类别属性值
        dates = html.xpath("//li[@class = 'find_main_li img find']")
        for event in dates:
            # eventItem = HudongbaItem()
            # eventItem['title'] = event.xpath("a/img[@class = 'hd_pic']/@title")[0]  # title
            # eventItem['description'] = ''
            # eventItem['address'] = event.xpath("div[@class = 'find_main_div']/div[@class = 'find_main_fixH']/div[@class = 'find_main_address']/p/a/text()")  # addres
            # eventItem['author'] = ""
            # eventItem['imageUrl'] = event.xpath("a/img[@class = 'hd_pic']/@data-src")[0]
            # print('000000000000')
            # print(eventItem['imageUrl'])
            # print('000000000000')
            # executable_path = "/Users/sinker/Documents/Phantomjs/bin/phantomjs"PhantomJS()
            # driver = webdriver.h   str(driver.get()
            # chrome_options = Options()
            # chrome_options.add_argument("--headless")
            url = event.xpath(".//a/@href")[0]
            request = scrapy.Request(url,self.process_Many,dont_filter=True)
            # request.meta['headless'] = True
            # print(url)
            # yield scrapy.Request(url,self.process_Many,dont_filter=True)
            yield request
            #
    #many msg
    def process_Many(self,response):
        result = redis.Redis(host='localhost', port=6379, decode_responses=True)
        # url = response.url
        # driver = webdriver.Chrome()
        # driver.get(url)
        # driver.save_screenshot('screen.png')
        # driver.page_source
        # demo = response.meta['demo']
        # print(demo)
        eventItem = HudongbaItem()
        resp = response.text
        #将以字串形式的xml进行取值
        soup = BeautifulSoup(resp, 'lxml')
        src = soup.select('head script')[6].string
        src_text = js2xml.parse(src,  debug=False)
        src_tree = js2xml.pretty_print(src_text)
        print('treeeeeeeeeeeeeeeeeeeeeeeeeeeee')
        # print(src_tree)
        selector = etree.HTML(src_tree)
        start = selector.xpath("//property[@name = '_oldStartDate']/string/text()")[0]
        print(start)
        print(len(start))

        end = selector.xpath("//property[@name = '_oldEndDate']/string/text()")[0]
        print(end)
        print(len(end))
        startDate = datetime.datetime.now().strftime('%Y-') + start
        endDate = datetime.datetime.now().strftime('%Y-') + end
        if (len(start) == 16):
            eventItem['startDate'] = start

        else:
            eventItem['startDate'] = startDate

        if (len(end) == 16):
            eventItem['endDate'] = end
        else:
            eventItem['endDate'] = endDate
        print('treeeeeeeeeeeeeeeeeeeeeeeeeeeee')

        html = etree.HTML(resp)

        eventItem['url'] = response.url
        str = html.xpath("//div[@class='content-body_head_l']/img/@alt")[0]
        eventItem['title'] = str.replace("互动吧-", "")
        eventItem['imageUrl'] = html.xpath("//div[@class='content-body_head_l']/img/@src")[0]
        eventItem['address'] = html.xpath("//div[@class='detail_Attr']/a/text()")[0]
        eventItem['author'] = ""
        eventItem['description'] = ""
        print('000000000000')
        print(eventItem['title'])
        print(eventItem['url'])
        print(eventItem['imageUrl'])
        print(eventItem['address'])
        print(eventItem['startDate'])
        print(eventItem['endDate'] )
        print('000000000000')
        yield eventItem
        en = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        result.set('hen', en)







