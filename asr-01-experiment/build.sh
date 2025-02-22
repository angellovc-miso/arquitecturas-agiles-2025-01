#!/bin/bash

docker pull gcc:13.2.0
docker pull node:20
docker pull python:3.10

docker-compose up --build -d
