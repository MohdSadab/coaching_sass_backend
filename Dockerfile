FROM python:3.9-slim
ENV PYTHONUNBUFFERED 1
# Install build dependencies (adjust based on your system)
RUN apt-get update && apt-get install -y build-essential libpq-dev
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/