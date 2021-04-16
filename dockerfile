FROM python:alpine3.12

WORKDIR /usr/src/app

COPY . .

CMD [ "python", "./client.py" ]