## Using Supervisor with Docker

通常情况下，一个docker container内只运行单个进程，例如一个只开启了ssh server的container。如果需要运行多个进程，可以把需要的启动命令都写到一个shell脚本内，也可以使用像supervisor的进程管理工具。






###[Supervisord](http://supervisord.org/introduction.html)


####安装

	pip install supervisor


####配置

通过 命令`echo_supervisor_conf` 创建一个默认配置文件
	
	echo_supervisord_conf > /etc/supervisord.conf


###uwsgi

需要注意uwsgi的版本（uWSGI 2.0.12 (64bit) ）

安装
	
	pip install uwsgi

启动uwsgi

		uwsgi --plugins /usr/lib/uwsgi/python_plugin.so  -s :8080 --wsgi-file world.py --callable app


启动uwsgi 后，访问 http://0.0.0.0:9090 出错
查看uwsgi日志输出

	invalid request block size: 21573 (max 4096)...skip

是因为 uwsgi -s 参数是以socket方式通信的，需要配置nginx进行代理。

