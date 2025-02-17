# Use the official MySQL image from the Docker Hub
FROM mysql:latest

# Set environment variables for MySQL
ENV MYSQL_ROOT_PASSWORD=admin
ENV MYSQL_DATABASE=portal
ENV MYSQLD_OPTS="--wait_timeout=28800 --interactive_timeout=28800 --max_connections=500"

# Copy the SQL dump files into the Docker container
COPY ./sql_dumps/init.sql /docker-entrypoint-initdb.d/

# Expose the default MySQL port
EXPOSE 3306
