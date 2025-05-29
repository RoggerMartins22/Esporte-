FROM python:3.10-slim

RUN apt-get update && apt-get install -y tzdata

RUN ln -fs /usr/share/zoneinfo/America/Sao_Paulo /etc/localtime && \
    dpkg-reconfigure --frontend noninteractive tzdata

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD uvicorn main:app --host 0.0.0.0 --port $PORT