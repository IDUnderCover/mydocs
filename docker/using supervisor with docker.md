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

配置文件


		<uwsgi>
		  <pythonpath>/home/chenjiebin/web/flaskdemo</pythonpath>
		  <module>flask</module>
		  <callable>app</callable>
		  <socket>127.0.0.1:5000</socket>
		  <master/>
		  <processes>4</processes>
		  <memory-report/>
		</uwsgi>


启动uwsgi
 
		sudo /usr/local/bin/uwsgi -x $(WD)/app_config.xml



		/usr/local/bin/uwsgi --http :9090 --wsgi-file world.py --callable app