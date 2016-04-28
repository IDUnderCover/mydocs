FROM alpine:latest

RUN apk --update add nginx python python-dev py-pip gcc libgcc && \
    pip install --upgrade pip && \
    pip install flask supervisor uwsgi
