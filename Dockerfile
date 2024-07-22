FROM python:latest

WORKDIR /src
COPY requirements.txt /src
RUN pip install -r requirements.txt
COPY . /src

CMD python3 /src/main.py
