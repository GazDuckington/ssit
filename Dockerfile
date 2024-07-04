FROM python:3.12-slim-bullseye
ENV TZ="Asia/Jakarta"

ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE ssit.settings

WORKDIR /app

RUN apt-get update

COPY requirements.txt /app/

RUN pip install -r requirements.txt

RUN apt install -y tzdata netcat

RUN ln -sf /usr/share/zoneinfo/Asia/Jakarta /etc/localtime

RUN pip freeze

COPY . .

EXPOSE 8000

RUN ls -lah

COPY ./entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

ENTRYPOINT ["sh", "-c", "/entrypoint.sh"]
