FROM python:latest

WORKDIR /src
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY /mongo /mongo
COPY /pyromember /pyromember
COPY .env .env
COPY config.py config.py
COPY main.py main.py

CMD python3 /src/main.py
