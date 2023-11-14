from django.shortcuts import render
from flask import Flask, request, jsonify, send_file, render_template, Response
from flask_restful import Api
import os
import subprocess
import glob
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import FileResponse, HttpResponse
from pydsstools.heclib.dss import HecDss
import numpy as np
import matplotlib.pyplot as plt

folder_path = '/WEBAPP'
app = Flask(__name__)
api = Api(app)
local_path = 'C:\\Users\\PatZh\\Desktop\\Paper_Lian\\docker\\file'
def get_running_container_id(container_name):
    try:
        command = f'docker ps -qf "name={container_name}"'
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, text=True)
        container_id = result.stdout.strip()
        return container_id
    except Exception as e:
        print(f"Error getting container ID: {e}")
        return None

container_id = get_running_container_id('hec-unsteady3')

# def upload_files(request):
#     if request.method == "POST":
#         files = request.FILES.getlist('files')
#         for file in files:
#             # 使用自定义的文件名 "Muncie"
#             file_path = handle_uploaded_file(file, folder_path, "Muncie")
#             os.system('docker cp {} {}'.format(file_path, container_id + ':' + folder_path))
#             os.remove(file_path)
#             # 設定Docker容器中檔案的權限
#         os.system('docker exec {} chown -R root:root {}'.format(container_id, folder_path))
#         return render(request, 'upload_done.html')
#     else:
#         return render(request, 'upload.html')

def upload_files(request):
    # 请求方法为POST时，进行处理
    if request.method == "POST":
        # 获取上传的文件，如果没有文件，则默认为None
        Files = request.FILES.getlist("files", None)
        if Files is None:
            return HttpResponse("無上傳文件")
        else:
            for f in Files:
                destination = open("/WEBAPP/" + f.name, 'wb+')
                for chunk in f.chunks():
                    destination.write(chunk)
                destination.close()
            return render(request, 'upload_done.html')
    else:
        return render(request, "upload.html")


# def handle_uploaded_file(file, folder_path, new_filename):
    # 获取上传文件的扩展名
    file_extension = os.path.splitext(file.name)[1]

    # 拼接新文件名
    new_file_name = new_filename + file_extension

    # 构建完整的文件路径
    file_path = os.path.join(folder_path, new_file_name)

    # 写入文件
    with open(file_path, 'wb') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    return file_path

    
def sim(request):
    subprocess.run(['./run-model.sh'], shell=True)
    
    return render(request, 'result.html')


def download_file1(request):
    # Create an application context
    with app.app_context():
        section_name = request.GET.get('section_name', '')
        run_plot2(section_name)
    file = open('/WEBAPP/fig1.png', 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="fig1.png"'
    return response
     
def download_file2(request):
    
    # Create an application context
    with app.app_context():
        run_plot()
        local_path = 'C:\\Users\\PatZh\\Desktop\\Paper_Lian\\docker\\file\\'
        os.system('docker cp {}:{} {}'.format(container_id, folder_path+'/fig1.png', local_path))

        # Open the local file and create a response
        with open(local_path+'\\fig1.png', 'rb') as file:
            response = Response(file.read(), content_type='application/octet-stream')
            response.headers['Content-Disposition'] = 'attachment; filename="fig1.png"'
            
        file = open('C:\\Users\\PatZh\\Desktop\\Paper_Lian\\docker\\file\\fig1.png', 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="fig1.png"'
    return render(request,'result.html')


def run_plot():
    dss_file = "Muncie.dss"
    pathname= "/White Muncie/*/LOCATION-FLOW/*/02JAN1900*/*/"
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

def run_plot2(section_name):
    section_index = int(section_name)
    # subprocess.run(['docker', 'exec', '-it', container_id, 'python', '/pydsstools/new-plot.py'], capture_output=True, text=True)
    dss_file = '/WEBAPP/Muncie.dss'
    pathname_pattern = "/*/*/LOCATION-FLOW/*/*/*/"
    x = []
    y = []
    
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

    
    plt.plot(x, y)
    plt.title('Flow Data')
    plt.xlabel('Times')
    plt.ylabel('Flow')
    plt.savefig('/WEBAPP/fig1.png')
# Create your views here.
