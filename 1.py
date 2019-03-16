import requests
import datetime
from bs4 import BeautifulSoup
import pymysql
#连接数据库 修改 端口 用户名 密码等（以MYSQL为例）
db=pymysql.connect(host="localhost",user="root",password="1123",port=3306,db="test")
cursor=db.cursor()
import pytesseract
from PIL import Image
import time,random
import urllib.request
import http.cookiejar
import re
from fake_useragent import UserAgent
# 国内机场三字代码
# AIR=['AHJ','YIE','AKU','AAT','NGQ','AKA','AQG','AOG','AVA','AYN','MFM','AEB','BSD','BAV','RLK','MFK','BHY','BJS','NAY','PEK','BFJ','BPL','CGQ','CGD','BPX','CSX','CIH','CZX','CHG','CTU','CIF','JUH','CKG','DLU','DDG','DCY','DQA','DAT','DAX','HXD','DIG','DOY','DNH','DLC','EJN','ENH','ERL','LCX','FUG','FYJ','FYN','FOC','KOW','KHH','GOQ','GYS','CAN','KWL','KWE','GYU','HRB','HAK','HLD','HMI','HDG','HGH','HZG','HCJ','HFE','HEK','HCN','HNY','HTN','HIA','HJJ','HUN','TXN','HTT','HET','HUZ','JMU','CYI','JGN','SWA','JIL','TNA','JIC','JDZ','JGS','JNG','JNZ','JIU','JZH','JXA','KJI','KGT','KHG','KRY','KCA','KRL','KMG','LXA','LYG','LLB','LJG','LNJ','LFQ','LXI','LYI','LZY','HZH','LPF','LZH','LYA','LZO','LLV','LUM','NZH','MXZ','MIG','OHE','MDG','KHN','NAO','LZN','NKG','NNG','YXG','NTG','NNY','NGB','NLH','PIF','SYM','IQM','CMJ','TAO','IQN','SHP','NDG','JJN','JUZ','RIZ','SYX','SHH','SHA','PVG','SQD','KNH','HSC','HPG','SHE','SZX','SHF','SJW','WDS','TPE','TTT','TNN','TYN','TXG','RMQ','HYN','TVS','TCZ','TSN','THQ','TNH','TGO','TEN','TLQ','WEF','WEH','WNH','WNZ','WUA','WUH','UCB','HLH','URC','WUX','WUS','WUZ','XMN','HKG','XFN','SIA','XIC','XIL','XNT','ACX','XNN','WUT','JHG','XUZ','YNZ','YTY','YNJ','YNT','YBP','YIH','LDS','YIC','INC','YKH','YIN','YIW','LLF','RHT','UYN','YCU','YUS','ZQZ','YZY','ZHA','ZAT','CGO','ZHY','HSN','ZUH','ZYI','AXF']

cj = http.cookiejar.MozillaCookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
urllib.request.install_opener(opener)
ua = UserAgent()
HEADER = {
    "Host": "www.variflight.com",
    'User-Agent':ua.random,
    # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:46.0) Gecko/20100101 Firefox/46.1",
#"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36"
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Connection": "keep-alive",
    "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
    "Connection": "keep-alive",
    "Cache-Control": "max-age=0"
}
#设置循环日期
# start = '2018-01-01'
# end = '2019-01-01'
# delta = datetime.timedelta(days=1)
# datestart = datetime.datetime.strptime(start, '%Y-%m-%d')
# dateend = datetime.datetime.strptime(end, '%Y-%m-%d')
begin = datetime.date(2018,12,7)
end = datetime.date(2019,1,1)
d = begin
delta = datetime.timedelta(days=1)
while d <= end:

    # 实际访问地址
    U = 'https://www.variflight.com/flight/SZX-PEK.html?AE71649A58c77&fdate='+d.strftime('%Y%m%d') #SZX PEK分别为出发地与目的地 在国内机场三字代码内可寻
    rt = urllib.request.urlopen(U)
    url = U
    print(U)
    r = requests.get(url, headers=HEADER)
    r.encoding = r.apparent_encoding
    html = r.text
    soup = BeautifulSoup(html, "html.parser")
    #获取当天航班次数
    if soup.find("h1"):
        c = soup.find("h1").find("span").getText()
        s = ((c[c.find("共") + 1:c.find("次")])) #实际航班数
    else:
        time.sleep(random.random() * 3)
        continue
    #图片识别
    html = rt.read().decode()
    imglist = re.findall('<img src="/flight/detail/([^"]+)"', html)
    ut = 'http://www.variflight.com/flight/detail/'
    #Tesseract-OCR目录 根据自己路径进行修改
    pytesseract.pytesseract.tesseract_cmd = 'D:/jTessBoxEditor/Tesseract-OCR/tesseract.exe' #建议使用自己训练过后的Tesseract目录，提高图像识别准确率
    i = 0
    for img in imglist:
        i += 1
        url = ut + img
        req = urllib.request.Request(url, None, HEADER)
        rt = urllib.request.urlopen(req)
        fw = open(str(i) + '.png', 'wb')
        fw.write(rt.read())
        fw.close()
    #遍历当日所有航班
    img = 1
    for index in range(int(s)):
        #航空公司
        t = soup.select('#list > li:nth-child(' + str((index + 1)) + ') > div > span.w260 > b > a:nth-child(1)')
        if len(t):
            print(t[0].text)
            a1 = t[0].text
        #航班号
        t = soup.select('#list > li:nth-child(' + str((index + 1)) + ') > div > span.w260 > b > a:nth-child(2)')
        if len(t):
            print(t[0].text)
            a2 = t[0].text
        #计划起飞时间
        t = soup.select('#list > li:nth-child(' + str((index + 1)) + ') > div > span:nth-child(2)')
        if len(t):
            print(t[0].text.strip())
            a3 = t[0].text.strip()
        #实际起飞时间
        t = soup.select('#list > li:nth-child(' + str((index + 1)) + ') > div > span:nth-child(3)')
        if t[0].text.strip() != '--':
            png='D://untitled1/' + str(img) +'.png'
            img = img + 1
            text = pytesseract.image_to_string(Image.open(png),lang='normal')
            print(text)
            a4 = text
        else:
            a4 = '--'
        #起飞机场
        t = soup.select('#list > li:nth-child(' + str((index + 1)) + ') > div > span:nth-child(4)')
        if len(t):
            print(t[0].text.strip())
            a5 = t[0].text.strip()
        #计划到达时间
        t = soup.select('#list > li:nth-child(' + str((index + 1)) + ') > div > span:nth-child(5)')
        if len(t):
            print(t[0].text.strip())
            a6 = t[0].text.strip()
        # 实际到达时间
        t = soup.select('#list > li:nth-child(' + str((index + 1)) + ') > div > span:nth-child(3)')
        if t[0].text.strip() != '--':
            png = 'D://untitled1/' + str(img) + '.png'
            img = img + 1
            text = pytesseract.image_to_string(Image.open(png), lang='normal')
            print(text)
            a7 = text
        else:
            a7 = '--'
        #到达机场
        t = soup.select('#list > li:nth-child(' + str((index + 1)) + ') > div > span:nth-child(7)')
        if len(t):
            print(t[0].text.strip())
            a8 = t[0].text.strip()
        # 准点率
        t = soup.select('#list > li:nth-child(' + str((index + 1)) + ') > div > span:nth-child(8)')
        if t[0].text.strip() != '--':
            png = 'D://untitled1/' + str(img) + '.png'
            img = img + 1
            text = pytesseract.image_to_string(Image.open(png), lang='normal')
            print(text)
            a9 = text
        else:
            a9 = '--'
        #当前状态
        t = soup.select('#list > li:nth-child(' + str((index + 1)) + ') > div > span.w150.gre_cor')
        if len(t):
            print(t[0].text)#到达
            a10 = t[0].text
        else:
            t = soup.select('#list > li:nth-child(' + str((index + 1)) + ') > div > span.w150.red_cor')
            if len(t):
                print(t[0].text)#取消
                a10 = t[0].text
            else:
                t = soup.select('#list > li:nth-child(' + str((index + 1)) + ') > div > span.w150.bla_cor')
                if len(t):
                    print(t[0].text)#提前取消
                    a10 = t[0].text
                else:
                    t = soup.select('#list > li:nth-child(' + str((index + 1)) + ') > div > span.w150.blu_cor')
                    if len(t):
                        print(t[0].text)  # 起飞
                        a10 = t[0].text
        #实际承运航班号
        t = soup.select('#list > li:nth-child(' + str((index + 1)) + ') > a.list_share')
        if len(t):
            print(t[0].get('title')[5:])
            a11 = t[0].get('title')[5:]
            sql = "insert into airinf(airline,number,projectoff,actualoff,departure,projectland,actualland,arrival,punctuality,AIRINFcol,Carrier,DATE) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql, (a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,datetime.datetime.strftime(d, '%Y-%m-%d')))
            db.commit()
        else:
            sql = "insert into airinf(airline,number,projectoff,actualoff,departure,projectland,actualland,arrival,punctuality,AIRINFcol,DATE) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql, (a1, a2, a3, a4, a5, a6, a7, a8, a9, a10,datetime.datetime.strftime(d, '%Y-%m-%d')))
            db.commit()
    d += delta
    time.sleep(3)#建议随机睡眠时间 防止频率过高
db.close()


