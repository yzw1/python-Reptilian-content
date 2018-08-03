#import mysql.connector
import pymysql
import pymysql.cursors
import redis
import scrapy
import datetime
from pymysql.converters import escape_string

from HuDongBa import settings

MYSQL_HOSTS = settings.MYSQL_HOSTS
MYSQL_USER  = settings.MYSQL_USER
MYSQL_PASSWORD = settings.MYSQL_PASSWORD
MYSQL_PORT     = settings.MYSQL_PORT
MYSQL_DB       = settings.MYSQL_DB

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

class Sql:

    @classmethod
    def insert_event(cls, title, description, startDate, endDate, address, author, url, imageUrl):
        result = redis.Redis(host='localhost', port=6379, decode_responses=True)
        print("sql::insert_event()")
        print(title)

        if(None == address):
            address = ''

        sql = "INSERT INTO HuDongBa (title, description, imageUrl, address, author, url, startDate, endDate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        print(">>> sql: ")
        print(sql)
        ret = cur.execute(sql, (title, description, imageUrl, address, author, url, startDate, endDate))

        print(ret)
        if(ret):

            sqls = 'select count(1) as num from HuDongBa '
            print(">>> sqls: ")
            rets = cur.execute(sqls)
            print(rets)

            rs = cur.fetchall()
            for r in rs:
                print(r['num'])
                result.set('hnum',r['num'])
        else:
            result.set('hnum',0)

        Error= result.get('herror')

        if(Error):
            CrawlerStatus = 1
        else:
            CrawlerStatus = 0
        if(ret):
            RecordNum = int(result.get('hnum')) - int(result.get('hdas'))
        else:
            RecordNum = 0
        print('00000000000000')
        print(CrawlerStatus)
        print('1111111111111111111111')


        print('1111111111111111111')
        print(RecordNum)
        print('2222222222222222')

        id = result.get('hid')
        print('333333333333333')
        print(id)
        print('44444444444444444444')
        EndTime = result.get('hen')
        print('5555555555555555')
        print(EndTime)
        print('6666666666666666')
        # EndTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        date = cur.execute('UPDATE CrawlerLog SET RecordNum = %s,Error = %s,CrawlerStatus= %s,EndTime = %s WHERE id = %s', (RecordNum,Error,CrawlerStatus,EndTime,id))
        print('%%%%%%%%%%%%%%%%%%%%%%%%')
        print(date)
        print('rrrrrrrrrrrrrrrreeeeeeeeeee')
        cnx.commit()



