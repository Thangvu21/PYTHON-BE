FROM python:3.11-slim

WORKDIR /PythonBE

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY ./src /PythonBE/src  

COPY .env . 
# Để tận dụng tối đa tính bất đồng bộ, hãy chạy Celery worker với event loop (ví dụ: gevent hoặc eventlet). Celery worker mặc định chạy với prefork, không hỗ trợ asyncio tốt
CMD ["celery", "-A", "src.core.celery:celery", "worker",  "-P gevent", '--loglevel=info', '--concurrency=200']
# , '--pool=gevent'
# celery -A src.core.celery:celery worker --loglevel=info --pool=gevent