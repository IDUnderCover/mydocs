##Fleet 跨节点调度服务

####简介
systemd作为init，可以管理一个节点的服务，使用 `--host` 也可管理远程节点的服务，但节点间必须要添加 `ssh-key`，而且功能也有限制。通过`Fleet`，可以把 整个CoreOS集群当作一台服务器来管理，即把`Fleet`作为分布式系统的init进程。


####安装部署

使用vagrant cloudinit自动组建CoreOS集群，设置好 userdata 和 config.rb 就可以

####基本命令

	# 列出集群节点
	core@core-01 ~ $ fleetctl list-machines
	MACHINE		IP		METADATA
	3547a4df...	172.17.8.103	-
	bc311683...	172.17.8.101	-
	fc45f283...	172.17.8.102	-


META是在创建节点前，userdata的meta字段中设置，当作标签，可与X-Fleet配合使用，简化集群管理。


用`Fleet`启动`hello.service`服务

	$ cat hello.service
	[Unit]
	Description=hello world
	After=docker.service
	Requires=docker.service
	
	[Service]
	TimeoutStartSec=0
	ExecStartPre=-/usr/bin/docker kill busybox1
	ExecStartPre=-/usr/bin/docker rm busybox1
	ExecStartPre=-/usr/bin/docker pull busybox
	ExecStart=/usr/bin/docker run --name busybox1 busybox /bin/sh -c "while true; do echo hello world; done"
	ExecStop=/usr/bin/docker stop busybox1
	ExecStopPost=/usr/bin/docker rm busybox1
	
	[X-Fleet]
	X-Conflicts=hello*.service
	
	[Install]
	WantedBy=multi-user.target
	

	core@core-01 ~/service $ fleetctl start hello.service 
	Unit hello.service inactive
	Unit hello.service launched on 3547a4df.../172.17.8.103
 

	core@core-01 ~/service $ fleetctl list-units
	UNIT		MACHINE				ACTIVE	SUB
	hello.service	3547a4df.../172.17.8.103	active	running

hello.service 成功在 3547 节点上成功运行，在该节点执行systemctl list-units 可以查看到hello service的运行情况。

####Fleet服务生命周期

1. 提交阶段
使用 fleetctl submit 将 unit 文件添加到 fleet 的记录缓存中， 此步骤没有涉及到 systemd，添加完成后表明此unit文件已被注册。如果要修改unit文件，修改完后需要重新 submit ， 和 systemd 的 deam reload 相似。

2. 加载服务
根据 unit 的 X-fleet  配置，选择好合适的节点，将服务unit文件传递到该节点。

3. 启动服务
fleetctl start hello 相当于 在上步所选的节点上启动 systemctl start hello.service

Fleet 相对应的命令为
submit  -> load -> start 
destroy -> unload -> stop




####ssh-agent 添加
	core@core-01 ~/.ssh $ eval `ssh-agent`
	Agent pid 2062
	core@core-01 ~/.ssh $ ssh-add id_rsa
	Identity added: id_rsa (id_rsa)
	core@core-01 ~/.ssh $ ssh-add -l    
	2048 SHA256:wOEfwdAHMaNVxBLz/7SzBrSoBK8e389rxr0dq0WbcQ0 id_rsa (RSA)






Reference：
https://github.com/coreos/fleet
CoreOS 实践之路
