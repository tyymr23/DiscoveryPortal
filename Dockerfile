FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    lsb-release \
    python3.9 \
    python3-pip \
    nginx \
    dos2unix \
    mysql-server \
    redis-server

RUN curl -fsSL https://deb.nodesource.com/setup_16.x | bash - && \
    apt-get install -y nodejs

COPY entrypoint.sh /entrypoint.sh
RUN dos2unix /entrypoint.sh && chmod +x /entrypoint.sh

ENV MYSQL_ROOT_PASSWORD=admin
ENV MYSQL_DATABASE=portal
ENV MYSQLD_OPTS="--wait_timeout=28800 --interactive_timeout=28800 --max_connections=500"

COPY database/sql_dumps/init.sql /docker-entrypoint-initdb.d/
COPY database/sql_dumps/init.sql /database/sql_dumps/init.sql

EXPOSE 80
EXPOSE 443

RUN apt-get install -y python3.9 python3-pip

ENV PYTHONUNBUFFERED=1

WORKDIR /backend

COPY /backend/requirements.txt /backend/
RUN dos2unix /backend/requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

RUN pip install gunicorn
COPY /backend /backend
RUN find /backend -type f -exec dos2unix {} \;

COPY /backend/wait-for-it.sh /usr/local/bin/wait-for-it.sh
RUN dos2unix /usr/local/bin/wait-for-it.sh && chmod +x /usr/local/bin/wait-for-it.sh

COPY /backend/nginx.conf /etc/nginx/nginx.conf

RUN echo '#!/bin/bash\nnginx &\ngunicorn --workers 3 --worker-class gevent --timeout 0 -b 0.0.0.0:3001 run:app' > /start.sh
RUN chmod +x /start.sh

WORKDIR /frontend

COPY /frontend/package.json /frontend/package-lock.json ./
RUN npm install
COPY /frontend .
RUN npm run build

WORKDIR /
CMD ["/entrypoint.sh"]


