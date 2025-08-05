FROM python:3.11-slim

WORKDIR /PythonBE

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY ./src /PythonBE/src  

COPY .env . 

CMD ["celery", "-A", "src.core.celery:celery", "worker", '--loglevel=info']