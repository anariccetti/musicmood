FROM python:3.8.6-buster

WORKDIR /musicmood

COPY api.py .
COPY requirements.txt .
COPY models models/


RUN pip install --upgrade pip \
    && pip install -r requirements.txt

CMD uvicorn api:api --host 0.0.0.0