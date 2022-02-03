FROM python:3.8-slim

WORKDIR /app

RUN pip3 install --upgrade pip
RUN pip install requests
RUN pip install pandas
RUN pip install scikit-learn

