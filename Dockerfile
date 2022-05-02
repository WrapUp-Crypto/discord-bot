FROM python:3.8-slim-buster

COPY requirements.txt /opt/app/
RUN pip install --no-cache-dir -r /opt/app/requirements.txt

COPY src /app/src
WORKDIR /app

ENTRYPOINT ["python3", "-m", "src.bot"]