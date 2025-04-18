#!/bin/bash

service mysql start

service redis-server start

/usr/local/bin/wait-for-it.sh localhost:3306

mysql -u root -p"$MYSQL_ROOT_PASSWORD" < /docker-entrypoint-initdb.d/init.sql

mysql -u root -p$MYSQL_ROOT_PASSWORD <<EOF
USE mysql;
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '$MYSQL_ROOT_PASSWORD';
FLUSH PRIVILEGES;
EOF

service mysql restart

cd /backend

/start.sh

