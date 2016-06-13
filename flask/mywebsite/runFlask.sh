#!/bin/bash

app=$(docker run -d -p 80:80 -v $PWD/flask:/flask  \
	-v $PWD/nginx.conf:/etc/nginx/nginx.conf \
	-v $PWD/supervisord.conf:/supervisord.conf \
	nijialiang/website -c /supervisord.conf)
echo $app
