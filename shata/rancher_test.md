##Rancher

####资源分组，用户权限控制
一个Environment就是一个资源组（resource group），一个资源组可包含多台主机，通过Access Control 来赋予每个 Account 访问 Environment 的权限。  
例如可以创建一个测试用的 test 环境和开发用的 dev 环境，测试用户只能访问 test 环境，开发人员只能访问 dev 环境。

####多种容器调度框架
在创建新环境的时候，可以选择容器的编排框架（Container Orchestration）  


1. Cattle 

Rancher默认的框架，调度策略基本和swarm相同, 提供LB，DNS服务

2. Swarm

	可以通过在UI界面打开一个Terminal连接到主机的swarm-agent容器内，执行相关的docker 和docker-compose 命令
	测试过程中，可能由于网络原因，docker cli会时常出现连接不到docker daemon的情况


3. k8s
4. mesos


注意：如果当前主机有服务在运行，不能切换运行框架


####支持基础层面的监控

支持对主机以及每个容器的 CPU，Memory，Network，Storage读写的实时监控。  

![](http://i.imgur.com/dm5sftI.png)


####容器的基本操作

通过Rancher UI 基本都可以实现容器的CURD，scale 到多个 instance， `roll upgrade` 

可以通过在UI中打开一个shell来在container中执行相关命令，也可查看容器日志
![在jenkins container中 threaddump](http://i.imgur.com/OsAjnDI.png)


####Rancher对于通过native docker cli创建容器的管理

Rancher会实时的监控docker event事件流，任何的container的start，stop，destroy都会被rancher检测到加入到管理框架内。
（通过docker cli 创建的容器，只有在其started后才会被加入到Rancher的管理中，created的容器不会再Rancher UI中显示）


测试：  

在 rancher 主机上用 `docker cli` 创建一个 `ubuntu` 容器, `docker ps -a` 查看到容器（容器名为 `lonely_wing`）已被成功创建  


	cloud@dev-nijialiang-2:~$ docker ps -a
	CONTAINER ID        IMAGE                           COMMAND                  CREATED             STATUS                   PORTS                                          NAMES
	0b7eebfd6c98        ubuntu:14.04.3                  "/bin/bash"              4 seconds ago       Created                                                                 lonely_wing
	00426d3d4ddf        ubuntu:14.04.3                  "/bin/bash"              9 minutes ago       Up 9 minutes                                                            r-Default_test_1
	7475f46c5232        7cb4785fdc20                    "/bin/bash"              54 minutes ago      Up 54 minutes                                                           r-test


刚刚创建的容器并没有在 `Rancher UI` 界面中出现   

![](http://i.imgur.com/1k0N4rY.png)


启动该容器后，发现被加入到了Rancher中

	$ docker start -a lonely_wing

![](http://i.imgur.com/NLx2o0G.png)

--

####Rancher的 Managed Network
Rancher 内部提供了 overlay 网络用来实现 容器的跨主机访问。如果需要使用Rancher内部提供的LoadBalance 或者 DNS service 就必须加入该网络

docker cli 启动容器时 添加label标签即可将该容器加入Managed Network

	$ docker run -l io.rancher.container.network=true -itd ubuntu：14.04.3 bash

![](http://i.imgur.com/4AV8VnY.png)

容器成功加入了此网络

![](http://i.imgur.com/Sqs9nBt.png)

####使用Rancher 提供的Load Balance


docker-compose.yml
	
	httpserver:
	    ports:
	        - 8000
	    tty: true
	    image: python:2.7.12
	    command: ["python","-mSimpleHTTPServer"]


通过 UI 创建一个简单的 Stack

![](http://i.imgur.com/ZP7AHEq.png)

然后将container扩展到3个实例

![](http://i.imgur.com/f2AE4Un.png)

之后再为该httpserver Stack 增加一个 load balance

![](http://i.imgur.com/lRvJmhK.png)

为了测试lb的功能有效，我们在三个python httpserver 写入三个不同的文件

	httpserver_1 $ echo hello server 01 > name
	httpserver_2 $ echo hello server 02 > name
	httpserver_3 $ echo hello server 03 > name

在其他主机上执行以下命令，发现输出不同，证明lb成功运行

	cloud@dev-nijialiang-1:~$ curl  http://172.30.41.166:9898/name
	hello server 01
	cloud@dev-nijialiang-1:~$ curl  http://172.30.41.166:9898/name
	hello server 02
	cloud@dev-nijialiang-1:~$ curl  http://172.30.41.166:9898/name
	hello server 03


####Internal DNS Service

使用内部提供的DNS服务，根据以下两种方式可以访问指定服务

1. `service_name`.`stack_name`
2. `container_name`

![](http://i.imgur.com/YganLy8.png)


####Storage Service


####周期性同步
除了实时监控 `docker event stream` 外，Rancher也会周期性的与主机同步数据，为了避免在一些意外情况下，rancher 丢失了 docker 的 event 数据，从而造成数据不一致。



