FROM python:latest

WORKDIR /src
COPY requirements.txt /src
RUN pip install -r requirements.txt
COPY /mongo /src/mongo
COPY /pyromember /src/pyromember
COPY .env /src/.env
COPY config.py /src/config.py
COPY main.py /src/main.py

CMD python3 /src/main.py
