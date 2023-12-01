from pydsstools.heclib.dss import HecDss
import matplotlib.pyplot as plt
import numpy as np


dss_file = "C:\\Users\\PatZh\\Desktop\\xindian\\example.dss"
pathname = "/Tamsui xindaian//LOCATION-ELEV//02JAN1900 0250/RESULTS/"

def run_plot2(time_value):
    x = []
    y = []
    section_index = int(-time_value) 
    #因為矩陣是反的，所以索引值用負的。
    #例如:斷面0-77，矩陣[0]的數值就是斷面77
    dss_file = 'C:\\Users\\PatZh\\Desktop\\xindian\\example.dss'
    pathname_pattern = "/*/*/LOCATION-ELEV/*/*/*/"

    
    fid = HecDss.Open(dss_file)
    path_list = fid.getPathnameList(pathname_pattern, sort=1)
    
    for i in range(len(path_list)):
        pd = fid.read_pd(path_list[i])
        idx = pd.index.tolist()
        pd.insert(0, pd.index.name, idx)
        pd.index = range(1, pd.shape[0] + 1)
        np.array(idx)

        x.append(i)
        value = np.array(pd.iloc[:, 1].values)
        y.append(value[section_index])
        print(value)
    x1 = x[:-16]
    y1 = y[:-16]

    
    plt.plot(x1, y1)
    plt.title('Flow Data')
    plt.xlabel('Times')
    plt.ylabel('Flow')
    plt.savefig('fig1.png')
    plt.close()
    x = np.empty_like(x)
    y = np.empty_like(y)
    return y1[0]
print(run_plot2(27))