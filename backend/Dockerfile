# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /backend

# Install bash, dos2unix, nginx, and other dependencies
RUN apt-get update && apt-get install -y bash dos2unix nginx

# Copy the requirements file into the container
COPY requirements.txt /backend/

# Convert requirements.txt to LF line endings
RUN dos2unix /backend/requirements.txt

# Install the dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Install Gunicorn
RUN pip install gunicorn

# Copy the rest of the application code into the container
COPY . /backend/

# Convert all files in /backend to LF line endings
RUN find /backend -type f -exec dos2unix {} \;

# Copy the wait-for-it script
COPY wait-for-it.sh /usr/local/bin/wait-for-it.sh

# Ensure the wait-for-it script is executable and has LF line endings
RUN dos2unix /usr/local/bin/wait-for-it.sh && chmod +x /usr/local/bin/wait-for-it.sh

# Copy Nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Copy SSL certificates
# COPY certs /certs

# Create a start script
# RUN echo 'nginx && gunicorn --certfile=/certs/localhost.crt --keyfile=/certs/localhost.key --workers 3 --worker-class gevent --timeout 300 -b 0.0.0.0:3001 run:app' > /start.sh
RUN echo 'nginx && gunicorn --workers 3 --worker-class gevent --timeout 300 -b 0.0.0.0:3001 run:app' > /start.sh
RUN chmod +x /start.sh

# Expose the port that Nginx will listen on
EXPOSE 80
EXPOSE 443

# Set the default shell to bash
SHELL ["/bin/bash", "-c"]

# Command to run Nginx and Gunicorn
CMD ["wait-for-it.sh", "mysql_server:3306", "--", "/start.sh"]
