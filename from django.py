

import subprocess
import glob

from pydsstools.heclib.dss import HecDss
from pydsstools.heclib.dss.HecDss import Open
import numpy as np
import matplotlib.pyplot as plt
import h5py
import sys,io,os
from shutil import copyfile
def run_plot2(section_name):
    #因HEC-RAS中沒有指儲存單一斷面結果的路徑，因此另外撰寫
    #只繪製單一斷面結果的圖，由使用者輸入數字給定
    #目前限制不得輸入負數，若有需要得以在result.html中修改
    x = []
    y = []
    #更改字串數字格式
    section_index = int(section_name)
    #在獲取單一斷面之結果時陣列是反的，所以加上負號由後面開始取
    section_index = -section_index
    #目前.dss的名稱指定為example
    dss_file = 'C:\\Users\\PatZh\\Desktop\\xindian\\example.dss'
    #.dss指定的路徑格式，ELEV表示水位，FLOW表示流量
    pathname_pattern0 = "/*/*/LOCATION-ELEV/*/*/*/"
    pathname_pattern1 = "/*/*/LOCATION-FLOW/*/*/*/"

    fid = HecDss.Open(dss_file)
    
    #計數器，用來區分FLOW、ELEVATION的繪圖模式
    k = 1
    while k <= 2:
        fid = HecDss.Open(dss_file)
        if k == 1:
            path_list = fid.getPathnameList(pathname_pattern0, sort=1)
            TYPE = 'ELEV'
        else:
            path_list = fid.getPathnameList(pathname_pattern1, sort=1)
            TYPE = 'FLOW'
            
        for i in range(len(path_list)):
            pd = fid.read_pd(path_list[i])
            idx = pd.index.tolist()
            pd.insert(0, pd.index.name, idx)
            pd.index = range(1, pd.shape[0] + 1)
            np.array(idx)
            x.append(i)
            value = np.array(pd.iloc[:, 1].values)
            y.append(value[section_index])
            #x1、x2及y1、y2的修剪數目可能根據hec-ras版本會有變，需要注意
            #修剪的目的是，結果檔會有一些模擬時間之外的結果，例如:斷面最大水深等
            if k == 1:
                x1 = x[:-5]
                y1 = y[:-5]
                xobs = np.arange(0,25)
                obs = [3.29,3.31,3.3,3.2,3.06,3.04,3.04,3.07,3.08,3.03,3.04,3.2,3.29,3.24
                       ,3.22,3.21,3.23,3.25,3.24,3.25,3.27,3.26,3.2,3.01,3.18]
                plt.subplot(2,1, k)
                plt.plot(x1,y1,color = 'b',linewidth ='1')
                plt.title(f'NO.{section_name} {TYPE} Data')
                plt.xlabel('Times')
                plt.ylabel('ELEV')
                y1.to_csv('data.csv')
            else:
                x2 = x[:-5]
                y2 = y[:-5] 
                plt.subplot(2,1, k) 
                plt.plot(x2,y2,color = 'g',linewidth ='1')
                plt.title(f'NO.{section_name} {TYPE} Data')  
                plt.xlabel('Times')
                plt.ylabel('Flow')    
        x = []
        y = []      
        k = k + 1
    plt.tight_layout()
    plt.savefig('/WEBAPP/templates/image/fig1.png')
    plt.close()
# Create your views here.

run_plot2(27)