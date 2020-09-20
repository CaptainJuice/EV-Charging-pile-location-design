import requests
import  socket
import numpy as np
from folium.plugins import HeatMap
import folium
from tqdm import tqdm
import webbrowser
#部分代码来源:https://github.com/lbygg227/POI_GET/blob/master/POI_GET.py


timeout=20
ak='g5RmsmSTnZNyMmbcUBVcLMGdaMs1aGxH'#百度开发者平台申请的密匙 ，每日访问次数上限30万次

def getdata(url):   #针对单一url获取对应数据
    try:
        socket.setdefaulttimeout(timeout)
        html=requests.get(url)
        data=html.json()
        if data['results']!=None:
            for item in data['results']:
                    jname=item['name']#获取名称
                    jlat=item['location']['lat']#获取经纬度
                    jlon=item['location']['lng']
                    jarea=item['area']#获取行政区
                    jadd=item['address']#获取具体地
                    jadd=jadd.replace(',','')
                    LOC.append([float(str(jlat)),float(str(jlon))])
                    LAT.append(float(str(jlat)))
                    LNG.append(float(str(jlon)))
                    j_str=jname+','+str(jlat)+','+str(jlon)+','+jarea+','+jadd+','+'\n'#字符串格式写入文件
                    if jarea==section:
                        f.write(j_str)
    except:
        getdata(url)

def method_bounds(lat_l,lng_l,lat_r,lng_r):    # 按经纬度范围查询POI
    #左下角纬度，左下角经度,右上角纬度,右上角经度
    lng_c=lng_r-lng_l#经度范围
    lat_c=lat_r-lat_l#纬度范围
    lng_num=int(lng_c/0.1)+1 #网格化处理
    lat_num=int(lat_c/0.1)+1
    arr=np.zeros((lat_num+1,lng_num+1,2))
    for lat in range(0,lat_num+1):
        for lng in range(0,lng_num+1):
            arr[lat][lng]=[lng_l+lng*0.1,lat_l+lat*0.1]

    urls=[] #url列表（分页访问）
    print('开始...')
    #地区划分
    for lat in range(0,lat_num):
        for lng in range(0,lng_num):
            for b in range(0,20):
                page_num=str(b) #获取页码，构建url
                #official example:http://api.map.baidu.com/place/v2/search?query=银行&
                # bounds=39.915,116.404,39.975,116.414&output=json&ak={您的密钥} //GET请求
                url='http://api.map.baidu.com/place/v2/search?query='+name+'&bounds='+str((arr[lat][lng][1]))+','+str((arr[lat][lng][0]))+','+str((arr[lat+1][lng+1][1]))+','+str((arr[lat+1][lng+1][0]))+'&page_size=20&page_num='+str(page_num)+'&output=json&ak='+ak
                urls.append(url)
    print ('url列表读取完成!...')
    L=len(urls)
    i=0
    for k in tqdm(range(L)):
        getdata(urls[i])
        i+=1
    f.close()
    print ('爬取完成!!')

print("区名： ")
section=input()
searchlist=['美食','酒店','购物','生活服务','丽人','旅游景点','休闲娱乐','运动健身','教育培训','文化传媒','医疗','汽车服务','交通设施','金融','房地产','公司企业','政府机构','出入口','自然地物','行政地标',] #来源：百度LBS云服务：http://lbsyun.baidu.com/index.php?title=lbscloud/poitags
"""
#平谷区经纬度范围
LG_min=116.9167 LG_max=117.40
LA_min=40.02 LA_max=40.37
"""
lng_l=116.9167
lng_r=117.40
lat_l=40.02
lat_r=40.37
for name in searchlist:
    print("【"+name+"】")
    f=open(r'C:\Users\l\Desktop\大创项目：EV\地图数据处理\POI-'+name+'.csv','a')#存储文件
    f.write('name,latitude,longtitude,srction,address\n')
    LOC=[];LAT=[];LNG=[]
    method_bounds(lat_l,lng_l,lat_r,lng_r)  #调用按经纬度范围查询POI
    m=folium.Map(location=[np.mean(LAT),np.mean(LNG)],zoom_start=10)  #绘制热力图，各点权值为1
    HeatMap(LOC).add_to(m)
    m.save(name+'.html') #保存为html文件
   # webbrowser.open(name,new=2)  #浏览器打开




