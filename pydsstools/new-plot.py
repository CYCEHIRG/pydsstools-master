# 單一斷面，除本行之外，以下註解皆為解釋上一行的程式碼
from pydsstools.heclib.dss import HecDss
import numpy as np
import matplotlib.pyplot as plt
dss_file = "C:\\Users\\PatZh\\Desktop\\Muncie.dss"

pathname_pattern ="/White Muncie/*/LOCATION-FLOW/*/02JAN1900*/*/"
x=[]
y=[]
fid = HecDss.Open(dss_file)


path_list = fid.getPathnameList(pathname_pattern,sort=1)
for i in range(len(path_list)):
    # 讀取所有模擬的時間點
    pd = fid.read_pd(path_list[i])
    # 讀取單一時間點
    idx = pd.index.tolist()
    pd.insert(0,pd.index.name,idx)
    pd.index = range(1,pd.shape[0] + 1)
    np.array(idx)
    # 上面四行總之是為了x及y而建，通常不會動，有要動再問

    x.append(i)
    # x軸為第幾個時間點，如果該模擬檔為5分鐘模擬一次，則為間隔第i個五分鐘
    value = np.array(pd.iloc[:,1].values)
    # 讀取水位or流量資料
    y.append(value[26])
    # 讀取該斷面於所有模擬時間點的流量or水位   

plt.plot(x,y)
plt.title('x')
plt.xlabel('Times')
plt.ylabel('Flow')
plt.savefig('fig1.png')