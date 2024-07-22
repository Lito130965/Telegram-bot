#FROM ubuntu:latest
#SHELL ["/bin/bash", "-c"]
#RUN apt-get update &&\
#    apt-get install -y python3 &&\
#    apt-get install python3-pip -y
#WORKDIR /home
#COPY * /home/
#RUN apt-get install python3-venv -y
#RUN python3 -m venv venv &&\
#    exit
#RUN source venv/bin/activate &&\
#    python3 -m pip install -r requirements.txt
#CMD ["python3", "./main.py"]


FROM python:latest

WORKDIR /src
COPY requirements.txt /src
RUN pip install -r requirements.txt
COPY . /src

CMD python3 /src/main.py
