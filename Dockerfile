# base image
FROM python:3.7

# set environment variables
ENV PYTHONUNBUFFERED 1

# setup environment variable
ENV DockerHOME=/lifenest

# set work directory
RUN mkdir -p $DockerHOME

# where your code lives
WORKDIR $DockerHOME

# copy content
ADD . $DockerHOME

# install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

