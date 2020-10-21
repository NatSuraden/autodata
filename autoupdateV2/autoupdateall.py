import requests  
from bs4 import BeautifulSoup
from datetime import date
import datetime
import time
import http.client
import psycopg2
go ="Y"
while go =="Y":
    nowdate = datetime.datetime.now()
    nowdate = nowdate.strftime("%H/%M/%S")
    nowdate = str(nowdate)
    if nowdate =="22/58/00":#<<<<run code ทิ้งไว้จะทำงานเองตามเวลา
        page = requests.get("https://xn--42cah7d0cxcvbbb9x.com/%E0%B8%84%E0%B9%88%E0%B8%B2%E0%B9%80%E0%B8%87%E0%B8%B4%E0%B8%99%E0%B8%9A%E0%B8%B2%E0%B8%97-%E0%B8%AA%E0%B8%A3%E0%B8%B8%E0%B8%9B%E0%B8%81%E0%B8%B2%E0%B8%A3%E0%B9%80%E0%B8%84%E0%B8%A5%E0%B8%B7%E0%B9%88%E0%B8%AD%E0%B8%99%E0%B9%84%E0%B8%AB%E0%B8%A7%E0%B9%80%E0%B8%87%E0%B8%B4%E0%B8%99%E0%B8%9A%E0%B8%B2%E0%B8%97%E0%B8%9B%E0%B8%A3%E0%B8%B0%E0%B8%88%E0%B8%B3%E0%B8%A7%E0%B8%B1%E0%B8%99-%E0%B8%A2%E0%B9%89%E0%B8%AD%E0%B8%99%E0%B8%AB%E0%B8%A5%E0%B8%B1%E0%B8%87/") 
        soup = BeautifulSoup(page.content, 'html.parser')
        data_list = soup.find_all("td")
        count = -1
        open_price =""
        now_price =""
        top_price =""
        low_price =""
        for i in data_list[0:5]:
            count += 1
            i = str(i)
            if count == 0:
                today = date.today()
                now = today.strftime("%d/%m/%y")
                now = str(now)
            elif count == 1:
                now_price += i[15:21]
            elif count == 2:
                open_price += i[4:10]
            elif count == 3:
                top_price += i[4:10]
            elif count == 4:
                low_price += i[4:10]
        page = requests.get("https://xn--42cah7d0cxcvbbb9x.com/") 
        soup = BeautifulSoup(page.content, 'html.parser')
        data_list = soup.find_all("td",class_="em bg-em g-u")
        #data_list = soup.find_all("td",class_="em bg-em g-d")
        hardsell = ""
        hardbuy = ""
        picsell = ""
        picbuy = ""
        count = -1
        for i in data_list:
            count += 1
            i = str(i)
            if count == 0:
                hardbuy += i[25:-5]
            elif count == 1:
                hardsell += i[25:-5]
            elif count == 2:
                picbuy += i[25:-5]
            elif count ==3:
                picsell += i[25:-5]
        today = date.today()
        now = today.strftime("%d/%m/%y")
        now = str(now)
        conn = http.client.HTTPSConnection("www.goldapi.io")
        payload = ''
        headers = {
                'x-access-token': 'goldapi-3o2nyukgc3rzcm-io',
                'Content-Type': 'application/json'
        }
        conn.request("GET", "/api/XAU/USD", payload, headers)
        res = conn.getresponse()
        data = res.read()
        data.decode("utf-8")
        a = data.decode("utf-8")
        a = a.split(",")
        lowprice = (a[7])[12:]
        highprice = (a[8])[13:]
        price = (a[10])[8:]
        today = date.today()
        D = today.strftime("%d/%m/%y")
        connection = psycopg2.connect(user="postgres",
                                    password="1234",
                                    host="127.0.0.1",
                                    port="5432",
                                    database="pythonlogin")
        cursor = connection.cursor()
        postgres_insert_query = """ INSERT INTO MoneyTHAPI (D_M_Y,open_price, high_price, low_price,now_price) VALUES (%s,%s,%s,%s,%s)"""
        cursor.execute(postgres_insert_query,(now,open_price,top_price,low_price,now_price))
        connection.commit()
        postgres_insert_query = """ INSERT INTO GoldTH (D_M_Y,hard_buy, hard_sell, pic_buy,pic_sell) VALUES (%s,%s,%s,%s,%s)"""
        cursor.execute(postgres_insert_query,(now,hardbuy,hardsell,picbuy,picsell))
        connection.commit()
        postgres_insert_query = """ INSERT INTO GoldAPI (D_M_Y, low_price, high_price,price_USD) VALUES (%s,%s,%s,%s)"""
        cursor.execute(postgres_insert_query,(D,lowprice,highprice,price))
        connection.commit()
        cursor.close()
        connection.close()
        time.sleep(10)
            