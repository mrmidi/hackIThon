FROM python:3.8-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN mkdir /app
WORKDIR /app

RUN apk update && apk add python3-dev \
                          gcc \
                          build-base \
                          libffi-dev
RUN pip3 install --upgrade pip wheel
# RUN pip3 install setuptools wheel backports.zoneinfo
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . /app/

#EXPOSE 8000
#CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
