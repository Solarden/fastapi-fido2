FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11

ENV PYTHONUNBUFFERED 1

RUN apt update && apt upgrade -y
RUN apt install -y make

COPY requirements /requirements
RUN pip install -r /requirements/requirements.txt

WORKDIR /app
COPY . .
