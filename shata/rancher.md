##Rancher

### Install on a single node
	
	# start rancher server
	sudo docker run -d --restart=always -p 8080:8080 rancher/server
	
	# add an agent host
	sudo docker run -d --privileged -v /var/run/docker.sock:/var/run/docker.sock -v /var/lib/rancher:/var/lib/rancher rancher/agent:v1.0.2 http://172.30.41.158:8080/v1/scripts/927ECB401F914DCDDB62:1472007600000:0PRsTxqrgH2q9KmWd9nNLYQsM

### Infrastructure Service

Managed Network. secure overlay network using IPsec tunneling
Load balancer. HAProxy


### Image Push
![](http://i.imgur.com/tI9J1vy.png)




###HA

External Mysql DB

image mysql:5.7

	# 启动mysql容器
	docker run --name rancher-mysql -p 3306:3306 -v /home/shata/mysql:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=1234qwer -d mysql:5.7 

	# 创建数据库
	docker exec -ti rancher-mysql /bin/bash
	mysql -h localhost -uroot -p1234qwer
	create database rancher

	# 从镜像仓库拉取rancher/server
	sudo ros config set rancher.docker.args "['daemon','--insecure-registry','172.30.20.61:5000']"

	NOTE:
	For any changes made with `sudo ros config`, you must reboot for them to take effect.

	sudo reboot 
	docker pull 172.30.20.61:5000/rancher/server

	# 在第一台机子上启动完成后，浏览器进入8080，HA页面
	sudo docker run -d -p 8080:8080 \
	-e CATTLE_DB_CATTLE_MYSQL_HOST="172.30.20.61" \
	-e CATTLE_DB_CATTLE_MYSQL_PORT=3306 \
	-e CATTLE_DB_CATTLE_MYSQL_NAME="rancher" \
	-e CATTLE_DB_CATTLE_USERNAME=root \
	-e CATTLE_DB_CATTLE_PASSWORD=1234qwer \
	-v /var/run/docker.sock:/var/run/docker.sock \
	rancher/server




![](http://i.imgur.com/cxvGlkg.png)





![](http://cdn.rancher.com/wp-content/uploads/2016/05/06231843/2016.05.09-HA-v1.0.1-1024x576.jpg)


###Environment
根据Environment来划分资源使用，隔离基础环境和使用人群

比如创建了一个swarm environment