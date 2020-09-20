import pandas as pd
import numpy as np
import folium
import webbrowser
from folium.plugins import HeatMap
from tqdm import tqdm

#热值图可视化交通流量
#热力图存为html
#交通流量排名前20地点的经纬度和密度存为csv

area='平谷区'
name='北京_'+area+'.html'
path=r'C:\Users\l\Desktop\大创项目：EV\地图数据处理\OneDrive-2020-05-18\T-drive Taxi Trajectories\release\taxi_log_2008_by_id\\' #数据路径
#平谷区经纬度范围 （可修改）
#--------------------------------------------
LG_min=116.9167
LG_max=117.40
LA_min=40.02
LA_max=40.37
#--------------------------------------------
#建立地图
BJ_center=[(LA_min+LA_max)/2,(LG_max+LG_min)/2]
m=folium.Map(location=BJ_center,zoom_start=10)
gap=0.01  #表格大小
IND2=int((LG_max-LG_min)/gap)
IND1=int((LA_max-LA_min)/gap)
DATA=np.zeros((IND1,IND2))
#取前200辆车
sample_size=200
i=1
for k in tqdm(range(sample_size)):
    data=pd.read_csv(path+str(i)+r'.txt')
    LG=data['longtitude']
    LA=data['latitude']
    Comb=[]
    for j in np.arange(len(LG)):
        if LA[j]>=LA_min and LA[j]<=LA_max and  LG[j]>=LG_min and LG[j]<=LG_max:
            ind1=int((LA[j]-LA_min)/gap)
            ind2=int((LG[j]-LG_min)/gap)
            DATA[ind1-1,ind2-1]+=1
    i+=1
Final_data=[]
for i in np.arange(IND1):
    for j in np.arange(IND2):
        Final_data.append((LA_min+gap*(i+1),LG_min+gap*(j+1),int(DATA[i,j])))
HeatMap(Final_data).add_to(m)
Final_data.sort(key=lambda x: x[2],reverse=True)
Top20=Final_data[0:20]
for k in np.arange(20):
    content='location :('+str(round(Top20[k][1],4))+','+str(round(Top20[k][0],4))+")"+"\ndensity: "+str(Top20[k][2])
    folium.Marker(Top20[k][0:2],tooltip='click me for 【location】 and 【traffic density】',popup=content).add_to(m)
    print(Top20[k])
m.save(name)
webbrowser.open(name,new=2)
columns=['latitude','longtitude','density']
dt=pd.DataFrame(Top20,columns=columns)
dt.to_csv(area+"_csv.csv", index=0)


