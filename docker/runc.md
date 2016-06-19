##runc 

runc 是一个命令行工具，用来产生大量符合 OCI 标准的容器


###Building：
	
	#安装go
	$ apt-get install golang    # 版本必须1.6 以上 
	
	#新建一个go project, 在src目录下新建 github.com/opencontainers 目录
	$ cd github.com/opencontainers
	$ git clone https://github.com/opencontainers/runc
	$ cd runc

	# 安装 seccomp
	$ sudo apt-get install libseccomp-dev seccomp

	# 编译安装
	$ make && sudo make install 

###Using  runc

创建 OCI Bundle，[bundle](https://github.com/opencontainers/runtime-spec/blob/master/bundle.md)  也就是一个目录，包含了所有container运行所需的文件. 一个容器必须基于root filesystem，我们可以从docker container中提取出来
		
		# create the top most bundle directory
		$ mkdir /mycontainer
		$ cd /mycontainer

		# create the rootfs directory
		$ mkdir rootfs
		
		# 创建一个busybox容器，直接将其导出并解压到 rootfs文件夹下
		$ docker export $(docker create busybox) | tar -C rootfs -xvf -

接下来创建容器配置文件，`runc` 提供了一个命令直接生成一个基础配置模板

		$ runc spec

根据需要可自行修改 `config.json` 文件

###Running Containers

现在一个bundle目录下包含一个config.json 配置文件和 root filesystem.
	
	razaura@ubuntu-home:~/mycontainer$ ls
	config.json  rootfs

	# 启动container
	razaura@ubuntu-home:~/mycontainer$ sudo runc run mycontainerid
	/ #

	# 查看当前容器运行情况
	razaura@ubuntu-home:~/mycontainer$ sudo runc list
	ID                                                                 PID         STATUS      BUNDLE                                                                                       CREATED
	07f5e38f0c964932b79f36d36935d4443430f74f700313747ad0a1550d4a1a42   9239        running     /run/docker/libcontainerd/07f5e38f0c964932b79f36d36935d4443430f74f700313747ad0a1550d4a1a42   2016-06-18T09:17:04.152716976Z
	7d927bf142272a6d1c6c66b5e4952831facae986992338592a7d88fd71d12665   22756       running     /run/docker/libcontainerd/7d927bf142272a6d1c6c66b5e4952831facae986992338592a7d88fd71d12665   2016-06-18T14:23:31.701898651Z
	mycontainerid                                                      10838       running     /home/razaura/mycontainer                                                                    2016-06-18T15:55:16.99772038Z

第三个即为我们刚才所起动的容器，剩下的两个是通过docker daemon 来运行的，因为docker 也是基于`runc`。


		root@ubuntu-home:/usr/bin# ls -al | grep docker
		-rwxr-xr-x  1 root root    35204152 6月   2 06:01 docker
		-rwxr-xr-x  1 root root    14683048 6月   2 06:00 docker-containerd
		-rwxr-xr-x  1 root root    11058056 6月   2 06:00 docker-containerd-ctr
		-rwxr-xr-x  1 root root     2626680 6月   2 06:00 docker-containerd-shim
		-rwxr-xr-x  1 root root     9466784 6月   2 05:59 docker-runc




