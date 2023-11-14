FROM ghcr.io/osgeo/gdal:ubuntu-small-3.7.2

RUN apt-get -y update \
   && apt-get -y install wget \
    && apt-get -y install unzip

RUN apt-get -y install gfortran python3.10 python3-pip 

COPY . ../

RUN chmod +x ras/v61/*
#RUN chmod +x ras/Muncie/*
#RUN chmod +x ras/Muncie/wrk_source/*
RUN chmod +x WEBAPP/WEBAPP/*

RUN python -m pip install --upgrade pip
RUN python -m pip install --no-cache-dir --upgrade -r requirements.txt
RUN python setup.py install

# Entrypoint script
RUN chmod +x /script.sh
ENTRYPOINT [ "/script.sh" ]

#WORKDIR /ras/Muncie
#COPY ./run-model.sh .
#RUN chmod +x run-model.sh

WORKDIR /WEBAPP
RUN chmod +x run-model.sh
RUN chmod +x run-server.sh
ENV \
    PORT=5555 \
    HOST=0.0.0.0
EXPOSE 5555
CMD ["./run-server.sh"]











