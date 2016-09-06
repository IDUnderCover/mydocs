我目前是这么理解的  
1.在docker中运行的程序，命令行的输出怎么重定向到文件
  
在docker daemon 启动容器时，会创建一个goroutine来绑定容器内所有进程的标准输出描述符，当接收到输出时，goroutine立刻将这些内容写入到与容器ID对应的日志文件中`/var/lib/docker/containers/container_id.json_log`。这个是不是可以转化为docker 日志收集的问题。  
http://blog.daocloud.io/allen_docker01/


2.怎么查看运行在docker内的进程的状态，包括CPU，Memory，端口连接情况，IO情况

直接通过 `docker stats` 可以查看大部分的信息， 官方也提供了相应API
https://docs.docker.com/engine/reference/api/docker_remote_api_v1.24/#/get-container-stats-based-on-resource-usage  
现在docker 的监控工具有很多，我还要去多尝试一下。
![](http://i.imgur.com/E1ae87u.png)

3.环境变量与用户设置的变量在docker内部是什么样的情况

做Image的时候可以指定好变量，用户也可以在运行容器时设置环境变量。

	cloud@dev-nijialiang-1:~$ docker run -e NAME=SHATA -ti ubuntu:14.04 /bin/bash
	root@c6187ffec89c:/# env | grep NAME
	HOSTNAME=c6187ffec89c
	NAME=SHATA
