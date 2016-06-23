##CoreOS 集群搭建

1. 获取 Vagrant 文件
 
		git clone https://github.com/coreos/coreos-vagrant.git

2. 配置集群参数

	使用官方服务器的自动发现，获取token
		razaura@ubuntu-home:~/coreos-vagrant$ curl  http://discovery.etcd.io/new?size=3
		https://discovery.etcd.io/a17908370b37759167415ff0637a2762

