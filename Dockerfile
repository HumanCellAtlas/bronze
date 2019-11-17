# This file defines a docker image for bronze as a runtime
FROM python:3.6

RUN mkdir /bronze
WORKDIR /bronze

ADD bronze ./bronze
COPY setup.py ./
RUN pip install .
