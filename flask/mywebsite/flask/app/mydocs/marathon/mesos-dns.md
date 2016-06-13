##[Mesos-DNS](http://mesosphere.github.io/mesos-dns/docs/tutorial.html)



先从github上下载编译好的二进制包

	wget -O /usr/local/mesos-dns/mesos-dns https://github.com/mesosphere/mesos-dns/releases/download/v0.5.1/mesos-dns-v0.5.1-linux-amd64


创建配置文件`config.json`

	{
	  "zk": "zk://10.41.40.151:2181/mesos",
	  "refreshSeconds": 60,
	  "ttl": 60,
	  "domain": "mesos",
	  "port": 53,
	  "resolvers": ["169.254.169.254","10.0.0.1"],
	  "timeout": 5,
	  "email": "root.mesos-dns.mesos"
	}

其中 zk 为 mesos 地址，resolvers为解析mesos域外的dns服务器


由于mesos-mater 和 mesos-slave 都运行在docker内，需要将这两个文件 docker cp 到 container 内部


将 mesos-dns 运行在marathon上，避免服务不可用

mesos-dns的 marathon json 配置文件如下

	{
	"cmd": "sudo  /usr/local/mesos-dns/mesos-dns -config=/usr/local/mesos-dns/config.json",
	"cpus": 1.0, 
	"mem": 1024,
	"id": "mesos-dns",
	"instances": 1,
	"constraints": [["hostname", "CLUSTER", "2.3.4.5"]]
	}

注意需要将 mesos-dns和config.json 拷贝到mesos-salve容器内的/usr/local/mesos-dns目录下
constraints 配置项将限制 该容器只运行在装由 mesos-dns的机器上，也就是我们的mesos-slave。


启动Mesos-DNS容器

	curl -X POST -H "Content-Type: application/json" http://1.2.3.4:8080/v2/apps -d@mesos-dns.json


在 /etc/resolv.conf 添加mesos-dns的地址

	nameserver 192.168.1.88  #mesos-dns
	nameserver 8.8.8.8


运行一个nginx容器,json文件如下


	nginx.json

	{
	"id": "nginx",
	"container": {
	    "type": "DOCKER",
	    "docker": {
	        "image": "nginx:latest",
	        "network": "BRIDGE",
	        "portMappings":[
	            {   
	                "containerPort":80,
	                "hostPort": 0,
	                "protocol":"tcp"
	            }   
	        ]           
	    }   
	},
	"instances": 1,
	"cpus": 1,
	"mem": 640,
	"ports":[80]
	}


测试mesos-dns是否可用

	root@ubuntuServer:/# dig nginx.marathon.mesos

	; <<>> DiG 9.9.5-3ubuntu0.8-Ubuntu <<>> nginx.marathon.mesos
	;; global options: +cmd
	;; Got answer:
	;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 54716
	;; flags: qr aa rd ra; QUERY: 1, ANSWER: 2, AUTHORITY: 0, ADDITIONAL: 0
	
	;; QUESTION SECTION:
	;nginx.marathon.mesos.		IN	A
	
	;; ANSWER SECTION:
	nginx.marathon.mesos.	60	IN	A	172.17.0.14
	
	;; Query time: 0 msec
	;; SERVER: 192.168.1.88#53(192.168.1.88)
	;; WHEN: Thu May 05 21:33:53 CST 2016
	;; MSG SIZE  rcvd: 70


使用marathon的控制界面，将nginx scale 到 2 个instances

![](http://i.imgur.com/bFYFzbd.png)

	root@ubuntuServer:/# dig nginx.marathon.mesos
	
	; <<>> DiG 9.9.5-3ubuntu0.8-Ubuntu <<>> nginx.marathon.mesos
	;; global options: +cmd
	;; Got answer:
	;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 54716
	;; flags: qr aa rd ra; QUERY: 1, ANSWER: 2, AUTHORITY: 0, ADDITIONAL: 0
	
	;; QUESTION SECTION:
	;nginx.marathon.mesos.		IN	A
	
	;; ANSWER SECTION:
	nginx.marathon.mesos.	60	IN	A	172.17.0.14
	nginx.marathon.mesos.	60	IN	A	172.17.0.16
	
	;; Query time: 0 msec
	;; SERVER: 192.168.1.88#53(192.168.1.88)
	;; WHEN: Thu May 05 21:33:53 CST 2016
	;; MSG SIZE  rcvd: 70

可以看到nginx.marathon.mesos 对应着两个ip


	root@ubuntuServer:/# curl nginx.marathon.mesos
	<!DOCTYPE html>
	<html>
	<head>
	<title>Welcome to nginx!</title>
	<style>
	    body {
	        width: 35em;
	        margin: 0 auto;
	        font-family: Tahoma, Verdana, Arial, sans-serif;
	    }
	</style>
	</head>
	<body>
	<h1>Welcome to nginx!</h1>
	<p>If you see this page, the nginx web server is successfully installed and
	working. Further configuration is required.</p>
	
	<p>For online documentation and support please refer to
	<a href="http://nginx.org/">nginx.org</a>.<br/>
	Commercial support is available at
	<a href="http://nginx.com/">nginx.com</a>.</p>
	
	<p><em>Thank you for using nginx.</em></p>
	</body>
	</html>




