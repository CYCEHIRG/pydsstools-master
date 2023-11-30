from pydsstools.heclib.dss import HecDss
import matplotlib.pyplot as plt
import numpy as np


dss_file = "C:\\Users\\PatZh\\Desktop\\xindian\\example.dss"
pathname = "/White Muncie//LOCATION-FLOW//02JAN1900 0245/RESULTS/"

def run_plot2(section_name):
    x = []
    y = []
    section_index = int(section_name)
    # subprocess.run(['docker', 'exec', '-it', container_id, 'python', '/pydsstools/new-plot.py'], capture_output=True, text=True)
    dss_file = "C:\\Users\\PatZh\\Desktop\\xindian\\example.dss"
    pathname_pattern = "/*/*/LOCATION-FLOW/*/*/*/"

    
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
# Create your views here.

run_plot2('76')