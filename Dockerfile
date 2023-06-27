FROM ubuntu:20.04
ENV DEBIAN_FRONTEND=noninteractive
#RUN sed -i 's/archive.ubuntu.com/mirrors.cloud.tencent.com/g' /etc/apt/sources.list
RUN sed -i 's@//.*archive.ubuntu.com@//mirrors.ustc.edu.cn@g' /etc/apt/sources.list

RUN apt-get update && \
    apt-get install -y software-properties-common && \
    apt update
RUN apt-get update && apt-get install -y python3 python3-pip 
WORKDIR /app
COPY . /app
RUN pip3 install -r requirements.txt
CMD ["gunicorn", "--workers", "4", "--threads", "4", "--bind", "0.0.0.0:8888", "app:app"]

