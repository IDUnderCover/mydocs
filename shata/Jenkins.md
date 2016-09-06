## Jenkins

###Pipeline

基本概念：

Stage: 一个Pipeline可以划分为若干个Stage，每个Stage代表一组操作。注意，Stage是一个逻辑分组的概念，可以跨多个Node。  
Node: 一个Node就是一个Jenkins节点，或者是Master，或者是Agent，是执行Step的具体运行期环境。  
Step: Step是最基本的操作单元，小到创建一个目录，大到构建一个Docker镜像，由各类Jenkins Plugin提供。


### [Install jenkins plugins By hand](https://wiki.jenkins-ci.org/display/JENKINS/Plugins#Plugins-Byhand)
Save downloaded *.hpi/*.jpi file into $JENKINS_HOME/plugins





![](https://jenkins.io/images/post-images/need-for-pipeline/simple-cd-flow-small.png)




![](https://jenkins.io/images/post-images/need-for-pipeline/complex-cd-flow-small.png)


some tasks are run in one of the testing servers (yellow) while others are run on the production cluster(blue). While any task might produce an error, in some cases such an outcome triggers a separate set of tasks. Some parts of the flow are not liner and depend on task results. Some tasks should be executed in parallel to imporove the overal time required to run them. The list goes on and on.


 Often, we do not want only to create a job A that, once it’s finished running, executes job B, which, in turn, invokes job C. In real-world situations, things are more complicated than that. We want to run some tasks (let’s call them job A), and, depending on the result, invoke jobs B1 or B2, then run in parallel C1, C2 and C3, and, finally, execute job D only when all C jobs are finished successfully.



Start a jenkins node
	
	docker run -dP -v ~/jenkins_agent01:/var/jenkins_home --name=jenkins_agent01 jenkins:alpine


在单机中测试jenkins cluster 时， 首先基于 etcd 创建一个 overlay 网络, 配置docker daemon 的启动选项， 在其中指定etcd的地址


	DOCKER_OPTS="-H tcp://0.0.0.0:2375 -H unix:///var/run/docker.sock --cluster-store=etcd://127.0.0.1:2379 --cluster-advertise=127.0.0.1:2379"

	sudo service docker restart

	# 创建docker的overlay
	docker network create -d overlay jo # short for jenkins_overlay


然后启动三台agent(其中将agent03 作为了master)，将8080映射到宿主机的随机端口上，启动时需指定container使用overlay网络
	
	
	docker run -d -p 32888:8080  --net=jo -v ~/jenkins_agent01:/var/jenkins_home --name=jenkins_agent01 jenkins:alpine

![](http://i.imgur.com/9JeI17J.png)

<table>
	<tr>
		<td>NAME</td>
		<td>IP</td>
		<td>PORT</td>
	</tr>
	<tr>
		<td>agent01</td>
		<td>10.0.0.4</td>
		<td>50000</td>
	</tr>
	<tr>
		<td>agent02</td>
		<td>10.0.0.3</td>
		<td>50000</td>
	</tr>
	<tr>
		<td>agent03(master)</td>
		<td>10.0.0.2</td>
		<td>50000</td>
	</tr>
</table>


在 agent03上新建节点, 节点启动方法选择 `Launch agent via Java Web Start`

高级选项 `Tunnel connection through`中填写 agent03 overlay 地址的`ip:port` 

![](http://i.imgur.com/0bbfFnI.png)


在剩余的两个 `agent` 中执行以下命令， slave.jar需要下载，或者直接在启动agent的时候挂载volume

	java -jar slave.jar -jnlpUrl http://172.30.41.158:32890/computer/test/slave-agent.jnlp -secret e45dbe2b24ea6fe0b2cc905f431fa3a079183ebfcce115ca1722420f61dc45b5




执行完成后结果

![](http://i.imgur.com/ZgbHcI6.png)

其实不用 overlay网络也可以，  `Tunnel connection through` 填写master的 50000端口映射也行。


注意，container每次重启之后，ip 可能会变

![](http://i.imgur.com/jcGf65F.png)


Control how jenkins starts this agent


####jenkins in docker 



 	
 	
	echo deb http://apt.dockerproject.org/repo debian-jessie main > /etc/apt/sources.list.d/jessie-backports.list
	apt-get update
	apt-get install apt-transport-https ca-certificates
	apt-get install docker-engine



![](http://i.imgur.com/sQO7nna.png)

![](http://i.imgur.com/BlvJemO.png)


这样确实能够在宿主机上执行相关的docker 命令， 但是否会引起其他的安全问题，比如用户可以通过在jenkins中将`docker ps `命令填写到 `execute shell`,查看到该宿主机上所有的正在运行的container. 为了避免这一点，所有的构建只能通过dockerfile，不提供其他的命令。也就是daocloud和dockerhub的自动构建。



####Docker Registry的部署

	daocloud.io/library/registry              2.4.0               8b162eee2794        3 months ago        171.2 MB

	默认volume /var/lib/registry


####gitlab 

	docker pull sameersbn/gitlab:8.10.6

	wget https://raw.githubusercontent.com/sameersbn/docker-gitlab/master/docker-compose.yml

	docker-compose up 



compose `depends_on` filed

Express dependency between services, which has two effects:

docker-compose up will start services in dependency order. In the following example, db and redis will be started before web.
docker-compose up SERVICE will automatically include SERVICE’s dependencies. In the following example, docker-compose up web will also create and start db and redis.
Simple example:

	version: '2'
	services:
	  web:
	    build: .
	    depends_on:
	      - db
	      - redis
	  redis:
	    image: redis
	  db:
	    image: postgres
Note: depends_on will not wait for db and redis to be “ready” before starting web - only until they have been started. If you need to wait for a service to be ready, see [Controlling startup order](https://docs.docker.com/compose/startup-order/) for more on this problem and strategies for solving it.


在 gitlab 中创建了一个 repo，里面只有一个 Dockerfile
	
	FROM ubuntu:14.04
	ENTRYPOINT［"echo", "hello jenkins in docker"］

在jenkins 中创建一个新的项目，指定Git的地址


![](http://i.imgur.com/EHODTmT.png)

执行构建的结果

![](http://i.imgur.com/yjOYb7x.png)




###Gitlab CI




link jenkins slave

	$ip = docker inspect -f "{{.NetworkSettings.Networks.jenkinsdocker_default.IPAddress}}" jenkinsdocker_jenkins_master_1
	# 172.19.0.4

	# java -jar slave.jar -jnlpUrl http://172.19.0.4:8080/computer/agent-01/slave-agent.jnlp -secret c04bd455776a3fcecb31b3c7053678503c06140d6ad0c7959067235c232ab3b4



### 将potapi 组件连接到容器

	host 172.30.41.158

	cloud@dev-nijialiang-1:~/dockerfiles$ docker ps
	CONTAINER ID        IMAGE                                                  COMMAND                  CREATED             STATUS              PORTS                                                   NAMES
	ed095fc88cac        sameersbn/gitlab:8.10.6                                "/sbin/entrypoint.sh "   20 hours ago        Up 17 hours         443/tcp, 0.0.0.0:10022->22/tcp, 0.0.0.0:10080->80/tcp   gitlab_gitlab_1
	b735b6180b14        sameersbn/redis:latest                                 "/sbin/entrypoint.sh "   20 hours ago        Up 17 hours         6379/tcp                                                gitlab_redis_1
	1cd5035cd74c        sameersbn/postgresql:9.5-1                             "/sbin/entrypoint.sh"    20 hours ago        Up 17 hours         5432/tcp                                                gitlab_postgresql_1
	c9898a5812d1        daocloud.io/nijialiang/jenkins_docker:master-8893128   "/bin/tini -- /usr/lo"   3 days ago          Up 17 hours         50000/tcp, 0.0.0.0:32769->8080/tcp                      jenkinsdocker_jenkins_agent01_1
	7b2f2a1a6c7c        daocloud.io/nijialiang/jenkins_docker:master-8893128   "/bin/tini -- /usr/lo"   3 days ago          Up 17 hours         50000/tcp, 0.0.0.0:32768->8080/tcp                      jenkinsdocker_jenkins_agent02_1
	09cb4a683f77        daocloud.io/nijialiang/jenkins_docker:master-8893128   "/bin/tini -- /usr/lo"   3 days ago          Up 17 hours         50000/tcp, 0.0.0.0:32770->8080/tcp                      jenkinsdocker_jenkins_master_1




potapi 的 配置文件
	
		JENKINS_SERVER = {
	    'HOST': 'ci.shatacloud.com',
	    'PORT': 80,
	    'USER': 'shengtao.gao',
	    'PASSWORD': '1',
	    }
	
	DATABASE = {
	    'HOST': '172.30.40.140',
	    'NAME': 'tower_dev?charset=utf8',
	    'USER': 'tower',
	    'PASSWORD': 'towerpassword',
	    }
	
	GITLAB_SERVER = {
	    'HOST': 'git.shatacloud.com',
	    'PORT': '80',
	    'EMAIL': 'xuetao.hu@shatacloud.com',
	    'USER': 'cirobot',
	    'PASSWORD': 'devopsmadesimple',
	    }
	
	
	POTAPI_SERVER = {
	    'HOST': '172.30.40.135',
	    'LISTEN_IP': '0.0.0.0',
	    'PORT': 8081,
	    }
	
	HOOK_URL = 'http://%s:%s/api/job' % (POTAPI_SERVER['HOST'],
	                                     POTAPI_SERVER.get('PORT', 80))
	
	SOFTWARE_NAME_PREFIX = 'shata-'
	
	PYPI_SERVER = 'pypi.shatacloud.com:80'
	
	PYPI_SERVER = {
	    'HOST': 'pypi.shatacloud.com:80',
	    'USER': 'ci',
	    'PASSWORD': 'simple',
	}
	
	VIRTUALENV = '/opt/virtualenv/potapi'
	
	PROXY_IP = '172.30.51.127'
	
	WHITE_LIST = [
	  '172.30.51.120',
	  '172.30.51.141',
	]
	
	LDAP_SERVER={
	    'URL': 'ldap://172.30.51.145:389',
	    'ROOT_DN': 'cn=admin,dc=ldap,dc=shatacloud,dc=com',
	    'ROOT_PW': '0cda047d41081c041250',
	}




/etc/init/potapi/conf
/etc/potapi/setting.py
/root/.lic


