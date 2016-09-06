### Environment Replacement

if variable is not set, then the word will be the result

	${variable_name:-word} 

 if variable is set then word will be the result, otherwise the result is the empty string.

	${variable_name:+word}

###.dockerinore file



### RUN, CMD and ENTRYPOINT
shell form: normal shell processing, such as env variable substitution  
	
	ENV NAME Jack
	CMD echo "hello $NAME"
	>> hello Jack
 
exec form: avoid string munging

	CMD ["echo", "hello $NAME"]
	>> hello $NAME


### ARG
The `ARG` instruction defines a variable that users can pass at build-time using the `--build-arg <varname>=<value>`

	ARG user1=someone # set default value

`ENV` instruction always override and `ARG` instruction.

`ENV` values are always persisted in the built image.

	1 FROM ubuntu
	2 ARG CONT_IMG_VER
	3 ENV CONT_IMG_VER ${CONT_IMG_VER:-v1.0.0}
	4 RUN echo $CONT_IMG_VER

`ARG` variables do impact the build cache 


###[ONBUILD](https://docs.docker.com/engine/reference/builder/#/onbuild)

###STOPSIGNAL

###HEALTHCHECK

HEALTHCHECK [OPTIONS] CMD command


OPTIONS:
	
	--interval=DURATION(30s)
	--timeout=DURATION(30s)
	--retries=N(3)


### Docker Include
![](http://i.imgur.com/Dgqo51c.png)


###Notes:
[docker run vs cmd vs entrypoint](  
http://goinbigdata.com/docker-run-vs-cmd-vs-entrypoint/)