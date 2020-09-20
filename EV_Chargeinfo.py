import re
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import xlwt
import json
#爬取充电站信息：名称，地点，快充数量，慢充数量

def getcoord(addr,coordink): #调用高德开发平台API获得经纬度（每日限量访问300,000次）
    params={'key':'4bcde4e8a6e2a51ef79de6a977c4671a',
        'address':addr}
    res = requests.get(coordlink, params)
    jd = json.loads(res.text)
    try:
        return [jd['geocodes'][0]['location'].split(',')[0],jd['geocodes'][0]['location'].split(',')[1]]
    except:
        return [-1,-1]

coordlink='https://restapi.amap.com/v3/geocode/geo'
url='http://admin.bjev520.com/jsp/beiqi/pcmap/do/pcMap.jsp?name='+'北京' #北京市网址
url2='http://admin.bjev520.com/jsp/beiqi/pcmap/pages/pcmap_Left.jsp'     #Left部分
root='http://admin.bjev520.com'            #元页面网址
driver=webdriver.Chrome()                  #打开CHrome浏览器
driver.get(url)                            #进主页面
driver.get(url2)                           #进Left页面
soup=BeautifulSoup(driver.page_source,'html.parser')   #得到Left页面HTMLTEXT
P=soup.find_all('p')                       #查找名称
Name=[]
Longitude=[]
Latitude=[]
i=0
L=len(P)
print("充电桩名称+经纬度：")
for p in P:
    Name.append(p.string)
    OA=getcoord(p.string,coordlink)
    Longitude.append(OA[0])
    Latitude.append(OA[1])
    i+=1
    print("\r 进度:百分之%s"%(float(i)*100/L),end="")
print('\n获取名称完毕\n')
SPAN=soup.find_all('span')                 #查找地点
Address=[]
i=0
L=len(P)
print("充电桩位置描述：")
for span in SPAN:
    Address.append(span.string)
    i+=1
    print("\r 进度:百分之%s"%(float(i)*100/L),end="")
print('\n获取位置描述完毕\n')
A=soup.find_all('a')
Num=[]
i=0
L=len(A)
print("充电桩快充，慢充数量数量：")#查找快充数量和慢充数量
for a in A:
    link=a.get('href')
    link=root+link
    driver.get(link)
    new_soup=BeautifulSoup(driver.page_source,'html.parser')
    fast=0
    slow=0
    #正则表达式查询
    if new_soup.find_all(string=re.compile(r'快充数量：\d*个 ')):
        fast=str(new_soup.find_all(string=re.compile(r'快充数量：\d*'))[0]).split(':')[-1]
        fast=fast.split('：')[-1].split('个')[0]
    if new_soup.find_all(string=re.compile(r'慢充数量：\d*个 ')):
        slow=str(new_soup.find_all(string=re.compile(r'慢充数量：\d*'))[0]).split(':')[-1]
        slow=slow.split('：')[-1].split('个')[0]
    Num.append([fast,slow])
    i+=1
    #打印进度
    print("\r 进度:%s"%(float(i)*100/L),end="")
print('获取快慢充数量完毕')
#写入excel文件
f=xlwt.Workbook()
sheet1=f.add_sheet(u'sheet1',cell_overwrite_ok=True)
SUM=0
for name in Name:
    sheet1.write(SUM,0,name)
    sheet1.write(SUM,1,Address[SUM])
    sheet1.write(SUM,2,Num[SUM][0])
    sheet1.write(SUM,3,Num[SUM][1])
    sheet1.write(SUM,4,Longitude[SUM])
    sheet1.write(SUM,5,Latitude[SUM])
    SUM+=1
#excel文件每列内容：充电桩名称，位置描述，快充数量，慢充数量，经度，纬度(在文件第一行手动添加)
f.save('EV_Charging_Station.xls')
print("完成！！！")





