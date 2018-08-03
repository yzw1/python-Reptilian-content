import redis
import traceback
import pymysql
import pymysql.cursors
import redis
import scrapy
import sys
import datetime
from pymysql.converters import escape_string
from HuDongBa import settings
from .sql import Sql
from HuDongBa.items import HudongbaItem
from scrapy.shell import inspect_response

class HudongbaItemNewPipeline(object):

    def process_item(self, item, spider):
        # result = redis.Redis(host='localhost', port=6379, decode_responses=True)
        print("In process_item() ... ")
        #inspect_response(item, self)
        if isinstance(item, HudongbaItem):
            title       = item['title']
            description = item['description']
            address     = item['address']
            startDate   = item['startDate']
            endDate     = item['endDate']
            author      = item['author']
            url         = item['url']
            imageUrl    = item['imageUrl']
            # try:
            Sql.insert_event(title, description, startDate, endDate, address, author, url, imageUrl)
            # except Exception as e:
            #     # print(e)
            #     # print('eeeeeeeeeeeeeeeeeeeee')
            #     # Error = traceback.print_exc()
            #     s = traceback.extract_tb(sys.exc_info()[2])
            #     result.set('ess',s)
            #     result.set('es',e)
            #
            #     MYSQL_HOSTS = settings.MYSQL_HOSTS
            #     MYSQL_USER = settings.MYSQL_USER
            #     MYSQL_PASSWORD = settings.MYSQL_PASSWORD
            #     MYSQL_PORT = settings.MYSQL_PORT
            #     MYSQL_DB = settings.MYSQL_DB
            #
            #     config = {
            #         'user': MYSQL_USER,
            #         'password': MYSQL_PASSWORD,
            #         'host': MYSQL_HOSTS,
            #         'db': MYSQL_DB,
            #         'port': MYSQL_PORT,
            #         'charset': 'utf8mb4',
            #         'cursorclass': pymysql.cursors.DictCursor,
            #     }
            #     cnx = pymysql.connect(**config)
            #     cur = cnx.cursor()
            #     Locals = result.get('ess')
            #     print(Locals)
            #     Error = result.get('es')
            #     print(Error)
            #     print("sssssssssssssssssssss")
            #     CrawlerStatus = 1
            #     print(CrawlerStatus)
            #     print("22222222222222222222222")
            #     RecordNum = 0
            #     print(RecordNum)
            #     print('3333333333333333333333')
            #     id = result.get('id')
            #     print(id)
            #     print("iddiiiiiiiiiiiiiiiiiiiiiiiiii")
            #     EndTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            #     print(EndTime)
            #     print("11111111111111111111")
            #     date = cur.execute('UPDATE CrawlerLog SET RecordNum = %s,Error = %s,CrawlerStatus= %s,EndTime = %s,Locals = %s WHERE id = %s',(RecordNum, Error, CrawlerStatus, EndTime, Locals, id))
            #     print(date)
            #     print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            #     cnx.commit()
