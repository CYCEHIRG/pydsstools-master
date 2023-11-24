from pydsstools.heclib.dss import HecDss
import matplotlib.pyplot as plt
import numpy as np


dss_file = "C:\\Users\\PatZh\\Desktop\\Muncie.dss"
pathname = "/White Muncie//LOCATION-FLOW//02JAN1900 0245/RESULTS/"

fid = HecDss.Open(dss_file)
pd = fid.read_pd(pathname)


idx = pd.index.tolist()
pd.insert(0,pd.index.name,idx)
pd.index = range(1,pd.shape[0] + 1)
np.array(idx)
y = np.array(pd.iloc[:,1].values)
print(y)
plt.plot(idx,y)
plt.title(pathname)
plt.xlabel('Crosssections')
plt.ylabel('Flow')

plt.savefig('fig1.png')