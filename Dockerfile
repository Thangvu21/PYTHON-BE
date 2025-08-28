FROM python:3.11-slim

WORKDIR /PythonBE

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src /PythonBE/src
COPY .env .
COPY main.py .

# Expose port for FastAPI (optional, for documentation)
EXPOSE 8000

# No default CMD, docker-compose will override this for each service
