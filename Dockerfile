FROM ghcr.io/osgeo/gdal:ubuntu-small-3.8.1
#注意！這個模板時常更新，若沒辦法建立image就查看是否有更新
#論文撰寫時此模板版本為3.8.1，嫌麻煩可以把3.8.1改成latest，應該不會有問題

RUN apt-get -y update \
   && apt-get -y install wget \
    && apt-get -y install unzip

RUN apt-get -y install gfortran python3.10 python3-pip 
#複製同一層的所有檔案至Docker image
COPY . ./

RUN chmod +x ras/v61/*
RUN chmod +x WEBAPP/WEBAPP/*
RUN chmod +x WEBAPP/static/*

RUN python -m pip install --upgrade pip \
    && pip install --upgrade -r requirements.txt \
    && python setup.py install

# 甭管
RUN chmod +x /script.sh
ENTRYPOINT [ "/script.sh" ]

#指定工作路徑，這裡很重要，若有新增東西卻跑不了，可以檢查是否是因為檔案不在WEBAPP
WORKDIR /WEBAPP
#賦予檔案權限以使用
RUN chmod +x run-model.sh
RUN chmod +x run-server.sh
#指定port，以及ip，0.0.0.0表示不指定
ENV \
    PORT=5555 \
    HOST=0.0.0.0
EXPOSE 5555
#運行Django
CMD ["./run-server.sh"]











