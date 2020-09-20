from minisom import MiniSom
import numpy as np
import pandas as pd
from tqdm import tqdm
from sklearn.decomposition import PCA
import folium
import cmap
import webbrowser
import matplotlib.pyplot as plt
#平谷区经纬度范围 （可修改为其他区）
#--------------------------------------------
LG_min=116.9167
LG_max=117.40
LA_min=40.02
LA_max=40.37
#--------------------------------------------
# step1：data preparation
# （1）traffic flow
area='平谷区'
name='北京_'+area+'区域分类.html'
path1=r'C:\Users\l\Desktop\大创项目：EV\地图数据处理\OneDrive-2020-05-18\T-drive Taxi Trajectories\release\taxi_log_2008_by_id\\' #数据路径
BJ_center=[(LA_min+LA_max)/2,(LG_max+LG_min)/2]
gap=0.01  #单位表格大小
IND2=int((LG_max-LG_min)/gap)+1
IND1=int((LA_max-LA_min)/gap)+1
DATA=np.zeros((IND1,IND2))
sample_size=500
i=1
for k in tqdm(range(sample_size)):
    data=pd.read_csv(path1+str(i)+r'.txt')
    LG=data['longtitude']
    LA=data['latitude']
    for j in np.arange(len(LG)):
        if LA[j]>=LA_min and LA[j]<=LA_max and  LG[j]>=LG_min and LG[j]<=LG_max:
            ind1=int((LA[j]-LA_min)/gap)
            ind2=int((LG[j]-LG_min)/gap)
            DATA[ind1,ind2]+=1
    i+=1
Final_data1=[]
for i in np.arange(IND1):
    for j in np.arange(IND2):
        #LA_min+gap*(i),LG_min+gap*(j)
        Final_data1.append(int(DATA[i,j]))

# （2）POI
path2="C:/Users/l/Desktop/大创项目：EV/地图数据处理/POI_DATA/"
searchlist=['美食','酒店','购物','生活服务','丽人','旅游景点','休闲娱乐','运动健身','教育培训','文化传媒','医疗','汽车服务','交通设施','金融','房地产','公司企业','政府机构','出入口','自然地物','行政地标',] #来源：百度LBS云服务：http://lbsyun.baidu.com/index.php?title=lbscloud/poitags
paths=[path2+'POI-'+item+'.csv' for item in searchlist]
Final_data2=[[0]*len(searchlist) for i in range((IND1)*(IND2))]
kk=0
for path in paths:
    d=pd.read_csv(path,engine='python')
    DATA=np.zeros((IND1,IND2))
    for v in d.values:
        lat,lng=v[0],v[1]
        if lat>=LA_min and lat<=LA_max and  lng>=LG_min and lng<=LG_max:
            ind1=int((lat-LA_min)/gap)
            ind2=int((lng-LG_min)/gap)
            DATA[ind1,ind2]+=1
    for i in np.arange(IND1):
        for j in np.arange(IND2):
            Final_data2[i*IND2+j][kk]=(int(DATA[i,j]))
    kk+=1

#（3）Dimension reduction : PCA
X=np.array(Final_data2)
pca = PCA(n_components='mle',whiten=False)
pca.fit(X)
score=pca.explained_variance_ratio_
N=0
for i in range(len(score)):
    if(sum(score[0:i+1])>0.85):
        N=i
        break
T=pca.transform(X)
T=[(list(T[k][0:N])+[Final_data1[k]]) for k in range(len(list(T)))]

#Training ANN: Self_Organizing Mapping
som = MiniSom(6, 6, 6, sigma=0.3, learning_rate=0.5) # initialization of 6x6 SOM
som.train(T, 1000) # trains the SOM with 1000 iterations

#plot
loc=[som.winner(t) for t in T]
m=folium.Map(location=BJ_center,zoom_start=10)
kk=0
for item in loc:
    x,y=int(item[0]),int(item[1])
    color=cmap.getcolor((x-1)*6+y)
    lng=((kk%(IND2)))*gap+LG_min
    lat=(kk-(kk%(IND2)))/(IND2)*gap+LA_min
    p_location=[lat,lng]
    kk+=1
    print(p_location)
    folium.CircleMarker(location=p_location,radius=0.05,color=color,fill=True).add_to(m)
m.save(name)
webbrowser.open(name,new=2)










