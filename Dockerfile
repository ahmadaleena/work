FROM python:3.10-slim-bullseye

LABEL authors="saqib"

ENV PYTHONUNBUFFERED True
ENV APP_HOME /app

WORKDIR $APP_HOME

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . ./

VOLUME /data

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]