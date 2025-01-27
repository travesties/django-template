FROM python:3.11-alpine3.18 AS base

# prevents python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE=1
# prevents python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1


# update image and install necessary packages
RUN apk update
RUN apk add postgresql-client gcc python3-dev musl-dev linux-headers


WORKDIR /app


# Install required python packages
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install -U pytest

EXPOSE 8000

## Dev config
FROM base AS dev
COPY . /app/


## Debug config
FROM dev AS debug
RUN pip install debugpy
EXPOSE 5678


## Production config
FROM base AS production
RUN pip install gunicorn

## Docker runs container processes as root inside a container.
## We should change this in a production environment, because
## a malicious actor can gain root access to the Docker host
## if they manage to break out of the container. If you're not
## root in the container you'll be root on the host.
## TODO: Docker always sets volume mounts to root:root, which
## makes it impossible to collect django's static files
## as the app user. How can I do this as a non-root user?

# create app user
#RUN addgroup -S -g 1000 app && adduser -S -D -g '' -u 1000 app 

# setup working directory for app
ENV APP_HOME=/home/app/web
RUN mkdir -p $APP_HOME/static/

WORKDIR $APP_HOME

COPY . $APP_HOME

#USER app
