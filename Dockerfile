FROM python:3.9-alpine3.12

ENV WORKSPACE ${HOME}/workspace
RUN mkdir ${WORKSPACE}
WORKDIR ${WORKSPACE}

RUN apk update && apk add gcc postgresql-dev musl-dev

COPY ./requirements.txt ./requirements.txt
RUN python3 -m pip install -r requirements.txt

COPY ./app.py ./app.py
COPY ./bookstore ./bookstore
COPY ./fast_api ./fast_api
COPY ./templates ./templates
COPY ./static ./static
COPY ./migrations ./migrations
