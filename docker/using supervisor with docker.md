## Using Supervisor with Docker

通常情况下，一个docker container内只运行单个进程，例如一个只开启了ssh server的container。如果需要运行多个进程，可以把需要的启动命令都写到一个shell脚本内，也可以使用像supervisor的进程管理工具。

###[Supervisord](http://supervisord.org/introduction.html)


####安装

	pip install supervisor


####配置

创建一个配置文件
	
	echo_supervisord_conf > /etc/supervisord.conf