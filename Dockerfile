FROM python:3.9
ADD main.py .
COPY * .
RUN pip install requests beautifulsoup4 python-dotenv
CMD [“python”, “./main.py”]