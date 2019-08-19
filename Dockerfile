# This file defines a docker image for bronze as a runtime
FROM python:3.6

RUN mkdir /bronze
WORKDIR /bronze

COPY requirements.txt .

RUN pip install -r requirements.txt
