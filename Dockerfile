FROM python:3.7.2-alpine3.8
RUN apk update && apk upgrade && apk add bash
COPY .
CMD ["python", "main.py"]
