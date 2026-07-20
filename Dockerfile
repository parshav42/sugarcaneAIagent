#FROM ubuntu:latest
#LABEL authors="parshav"
#
#ENTRYPOINT ["top", "-b"]
#
#FROM python:3.12.3
FROM python:3.12-slim
WORKDIR /app

COPY requirements.txt  .

RUN pip install -r requirements.txt

COPY . .

EXPOSE  8003



CMD ["uvicorn","main:app","--host","0.0.0.0","--port","8001"]

