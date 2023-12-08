from pydsstools.heclib.dss import HecDss
from pydsstools.heclib.dss.HecDss import Open
import matplotlib.pyplot as plt
import numpy as np


dss_file = "C:\\Users\\PatZh\\Desktop\\xindian\\example.dss"
# pathname = "/Tamsui xindaian//LOCATION-ELEV//02JAN1900 0250/RESULTS/"
def run_plot2(section_name):
    x = []
    y = []
    section_index = int(section_name)
    section_index = -section_index
    dss_file = 'C:\\Users\\PatZh\\Desktop\\xindian\\example.dss'
    pathname_pattern0 = "/*/*/LOCATION-ELEV/*/*/*/"
    pathname_pattern1 = "/*/*/LOCATION-FLOW/*/*/*/"

    fid = HecDss.Open(dss_file)
    
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
            #x1及y1的修剪數目可能根據hec-ras版本會有變，需要注意
            if k == 1:
                x1 = x[:-5]
                y1 = y[:-5]
                plt.subplot(2,1, k)
                plt.plot(x1,y1,color = 'b',linewidth ='1')
                plt.title(f'NO.{section_name} {TYPE} Data')
                plt.xlabel('Times')
                plt.ylabel('Flow')
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
    plt.savefig('fig.png')
    plt.close()


run_plot2(27)