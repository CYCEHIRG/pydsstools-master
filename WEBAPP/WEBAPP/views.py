from django.shortcuts import render
from flask import Flask, request, jsonify, send_file, render_template, Response
from flask_restful import Api
import subprocess
import glob
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import FileResponse, HttpResponse
from pydsstools.heclib.dss import HecDss
from pydsstools.heclib.dss.HecDss import Open
import numpy as np
import matplotlib.pyplot as plt
import h5py
import sys,io,os
from shutil import copyfile

folder_path = '/WEBAPP'
app = Flask(__name__)
api = Api(app)

def upload_files(request):
    if request.method == "POST":
        Files = request.FILES.getlist("files", None)
        if Files is None:
            return HttpResponse("無上傳文件")
        else:
            for f in Files:
                destination = open("/WEBAPP/" + f.name, 'wb+')
                for chunk in f.chunks():
                    destination.write(chunk)
                destination.close()
            #以下為創建Linux版HEC-RAS模擬所需文件
            filename = 'example.p01.hdf'
            fsource = h5py.File(filename, 'r')
            fdest = h5py.File(os.path.splitext(filename)[0] + '.tmp.hdf', 'w')
            
            for fattr in  fsource.attrs.keys() :
                fdest.attrs[fattr]= fsource.attrs.get(fattr)
            
            for fg in  fsource.keys() :
                if fg != "Results" :
                    fsource.copy( fg, fdest )
            fdest.close()
            fsource.close()
            subprocess.run(['mv example.p01.tmp.hdf /WEBAPP/wrk_source/'], shell=True)
            #以上為創建Linux版HEC-RAS模擬所需文件
            return render(request, 'upload_done.html')
    else:
        return render(request, "upload.html")

    
def sim(request):
    subprocess.run(['./run-model.sh'], shell=True)
    # 由於建模時的設置問題，以Linux版本模擬後的.dss結果文件名可能會包含WINDOWS的路徑，為了確保能夠呼叫因此在這裡重新命名
    subprocess.run(['mv *.dss example.dss'], shell=True)
    #以下為獲取模擬結果的路徑，用於輸入
    dss_file = "/WEBAPP/example.dss"
    pathname_pattern = "/*/*/*/*/*/*/"
    with Open(dss_file) as fid:
        path_list = fid.getPathnameList(pathname_pattern, sort=1)
        result = []
        result.extend(path_list)
    
    return render(request, 'result.html', {'result': result})

def download_file1(request):
    with app.app_context():
        section_name = request.GET.get('section_name', '')
        run_plot2(section_name)
    file = open('/WEBAPP/fig1.png', 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="fig1.png"'

    return response
     
def download_file2(request):
    #總之跟download_file1()同理
    with app.app_context():
        time_value = request.GET.get('time_value', '')
        run_plot(time_value)
    file = open('/WEBAPP/fig1.png', 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="fig1.png"'
    return response


def run_plot(time_value):
    #本繪圖模組不會有問題，不用動
    #原定是用來繪製以時間為主體的水位或流量圖，現在變成繪製所有的結果
    #time_value是以網頁中的選單給定
    y = []
    dss_file = "/WEBAPP/example.dss"
    pathname= time_value
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
    plt.savefig('/WEBAPP/fig1.png')
    plt.close()
    y = np.empty_like(y)
    idx = np.empty_like(idx)


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
    dss_file = '/WEBAPP/example.dss'
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
                # xobs = np.arange(0,25)
                # obs = [3.29,3.31,3.3,3.2,3.06,3.04,3.04,3.07,3.08,3.03,3.04,3.2,3.29,3.24
                #        ,3.22,3.21,3.23,3.25,3.24,3.25,3.27,3.26,3.2,3.01,3.18]
                plt.subplot(2,1, k)
                plt.plot(x1,y1,color = 'b',linewidth ='1',label = 'sim')
                # line2, = plt.plot(xobs,obs,color = 'r', linewidth = '1',label = 'obs')
                # plt.legend(handles = [line1,line2],loc = 'upper right')
                plt.title(f'NO.{section_name} {TYPE} Data')
                plt.xlabel('Times')
                plt.ylabel('ELEV')
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
    plt.savefig('/WEBAPP/fig1.png')
    plt.close()
# Create your views here.
