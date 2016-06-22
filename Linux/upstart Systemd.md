## Upstart Systemd 

###Upstart
Ubuntu 的启动由upstart控制，自9.10后不再使用/etc/event.d目录的配置文件，改为/etc/init




###Systemd


![SysVinit](http://www.ibm.com/developerworks/cn/linux/1407_liuming_init3/image003.jpg  "SysVinit")

SysV  任务都是串行启动，Upstart 可将无依赖关系的任务并发运行


![systemd](http://www.ibm.com/developerworks/cn/linux/1407_liuming_init3/image005.jpg  "systemd")
而Systemd 即使项目间存在依赖关系，也能够并发执行, 利用 socket D-bus ,aufofs



Systemd分析系统状态命令，可参考 [Systemd - Fedora](https://fedoraproject.org/wiki/Systemd)
	
	#显示系统状态
	$ systemctl status

	# 输出激活单元，两条命令等价
	$ systemctl   
	$ systemctl list-units

	# 修改了unit文件后需重新载入
	$systemctl daemon-reload


（单元文件存放在 /usr/lib/systemd/system/ ， systemd 会先从 /etc/systemd/system/ 目录查找，systemctl enable docker.service 就是在 /etc/systemd/system/ 下创建一个软链接）

Unit是Systemd管理服务的基本单元，就如Upstart的service文件。Target是Systemd指定服务组启动的方式，就如Upstart的runlevel。下面创建一个应用服务，用docker 来启动一个busybox容器，并打印hello world

		#/etc/systemd/system/hello.service
		[Unit]
		Description=hello world  # unit 描述
		After=docker.service	   #在docker.service 之后运行
		Requires=docker.service  # 强依赖于docker.service
		
		[Service]
		TimeoutStartSec=0           #由于image的pull需要一段时间，关闭服务器动的超时检查
		ExecStartPre=-/usr/bin/docker kill busybox1   # 每个命令前都有 ‘  - ’符号，表示忽略错误输出
		ExecStartPre=-/usr/bin/docker rm busybox1    # ExecStartPre 表示 启动前先执行的命令
		ExecStartPre=-/usr/bin/docker pull busybox
		ExecStart=/usr/bin/docker run --name busybox1 busybox /bin/sh -c "while true; do echo hello world; done"
		ExecStop=/usr/bin/docker stop busybox1
		ExecStopPost=/usr/bin/docker rm busybox1
		
		[Install]
		WantedBy=multi-user.target         # 指定服务所属的target，等价于runlevel 3



下面启动 hello 服务

	# 需要从hub 上pull busybox 的image ，启动需要一段时间
	$ systemctl start hello.service

查看hello.service 的状态

	core-01 system # systemctl list-units hello*
	UNIT          LOAD   ACTIVE SUB     DESCRIPTION
	hello.service loaded active running hello world

	$ systemctl status hello
		hello.service - hello world
		   Loaded: loaded (/etc/systemd/system/hello.service; disabled; vendor preset: disabled)
		   Active: active (running) since Tue 2016-06-21 16:44:00 UTC; 31s ago
		  Process: 1323 ExecStartPre=/usr/bin/docker pull busybox (code=exited, status=0/SUCCESS)
		  Process: 1316 ExecStartPre=/usr/bin/docker rm busybox1 (code=exited, status=1/FAILURE)
		  Process: 1302 ExecStartPre=/usr/bin/docker kill busybox1 (code=exited, status=1/FAILURE)
		 Main PID: 1343 (docker)
		    Tasks: 5
		   Memory: 9.9M
		      CPU: 111ms
		   CGroup: /system.slice/hello.service
		           └─1343 /usr/bin/docker run --name busybox1 busybox /bin/sh -c while true; do echo hello world; done
		
		Jun 21 16:44:23 core-01 docker[1343]: hello world
		Jun 21 16:44:23 core-01 docker[1343]: hello world
		Jun 21 16:44:23 core-01 docker[1343]: hello world
		Jun 21 16:44:23 core-01 docker[1343]: hello world
		Jun 21 16:44:23 core-01 docker[1343]: hello world
		Jun 21 16:44:23 core-01 docker[1343]: hello world
		Jun 21 16:44:23 core-01 docker[1343]: hello world
		Jun 21 16:44:23 core-01 docker[1343]: hello world
		Jun 21 16:44:23 core-01 docker[1343]: hello world
		Jun 21 16:44:23 core-01 docker[1343]: hello world
	
设置开机自启动

	core-01 # systemctl enable hello.service
	Created symlink from /etc/systemd/system/multi-user.target.wants/hello.service to /etc/systemd/system/hello.service.


为什么我们没有在控制台看到 hello world 的输出？而通过状态查看可以看到部分输出，因为systemd通过journald将其重定向到了日志文件里。

日志文件都是二进制格式，通过 journalctl 可查看日志信息

	# 查看hello的日志
	core-01 multi-user.target.wants # journalctl --unit hello
	-- Logs begin at Sat 2016-06-11 06:59:52 UTC, end at Tue 2016-06-21 16:56:54 UTC. --
	Jun 21 16:43:20 core-01 systemd[1]: Starting hello world...
	Jun 21 16:43:20 core-01 docker[1302]: Failed to kill container (busybox1): Error response from daemon: Cannot kill container busybox1: No such container: 
	Jun 21 16:43:20 core-01 docker[1316]: Failed to remove container (busybox1): Error response from daemon: No such container: busybox1
	Jun 21 16:43:20 core-01 docker[1323]: Using default tag: latest
	Jun 21 16:43:37 core-01 docker[1323]: latest: Pulling from library/busybox
	Jun 21 16:43:37 core-01 docker[1323]: 385e281300cc: Pulling fs layer
	Jun 21 16:43:37 core-01 docker[1323]: a3ed95caeb02: Pulling fs layer
	Jun 21 16:43:53 core-01 docker[1323]: a3ed95caeb02: Verifying Checksum
	Jun 21 16:43:53 core-01 docker[1323]: a3ed95caeb02: Download complete
	Jun 21 16:44:00 core-01 docker[1323]: 385e281300cc: Verifying Checksum
	Jun 21 16:44:00 core-01 docker[1323]: 385e281300cc: Download complete
	Jun 21 16:44:00 core-01 docker[1323]: 385e281300cc: Pull complete
	Jun 21 16:44:00 core-01 docker[1323]: 385e281300cc: Pull complete
	Jun 21 16:44:00 core-01 docker[1323]: a3ed95caeb02: Pull complete
	Jun 21 16:44:00 core-01 docker[1323]: a3ed95caeb02: Pull complete
	Jun 21 16:44:00 core-01 docker[1323]: Digest: sha256:4a731fb46adc5cefe3ae374a8b6020fc1b6ad667a279647766e9a3cd89f6fa92
	Jun 21 16:44:00 core-01 docker[1323]: Status: Downloaded newer image for busybox:latest
	Jun 21 16:44:00 core-01 systemd[1]: Started hello world.
	Jun 21 16:44:00 core-01 docker[1343]: hello world
	Jun 21 16:44:00 core-01 docker[1343]: hello world
	Jun 21 16:44:00 core-01 docker[1343]: hello world
	Jun 21 16:44:00 core-01 docker[1343]: hello world
	Jun 21 16:44:00 core-01 docker[1343]: hello world
	Jun 21 16:44:00 core-01 docker[1343]: hello world
	Jun 21 16:44:00 core-01 docker[1343]: hello world
	Jun 21 16:44:00 core-01 docker[1343]: hello world
	Jun 21 16:44:00 core-01 docker[1343]: hello world
	Jun 21 16:44:00 core-01 docker[1343]: hello world

这样hello 服务不停的在后台打印日志，日志所占空间肯定非常大，可以通过修改 /etc/systemd/journald.conf 的 SystemMaxUse来限制最大使用。


在刚创建完 hello.service unit时，通过命令 systemctl list-units 是查看不到 hello 单元的，因为他还没有被激活，他还只是以文件形式存在着，通过 start 或 enable则可激活该单元。

由于systemd的缓存，修改了unit文件，需要daemon-reload，那么删除了一个unit文件，需要systemctl reset-failed 才可以将删除的unit 彻底删除。

在写unit的时候需要注意，在ExecStop和ExecStart等使用linux命令需要写出完整路径。


####定时器（.time结尾）
Unit 文件有一个特别的字段Timer，定义了定时器的触发时机和触发任务。
定时器触发时机
1. OnActiveSec，当自己被启动后的数秒
2. OnBootSec，当主机启动后
3. OnStartupSec，当操作系统启动完成后
4. OnUnitActiveSec，当指定服务被启动后
5. OnUnitInactiveSec，当指定服务停止后
6. OnCalendar，使用日历时间，在特定日期

为了避免大量任务在同一时间启动，设置触发精度 AccuracySec ，使任务在一个时间范围内启动


####路径监控器（.path）
Path 段
1.PathExitst: 如果该路径存在，则触发任务
2.pathExistsGlob：同上，但可用通配符
3.PathChanged：该目录，文件被修改了
4.PathModified：文件修改后
5.DeirectoryNotEmpty：目录不为空

####数据监控器（.socket）
用来监控系统的指定TCP/UDP端口、消息队列等。一旦有数据到来就触发启动指定服务。

Socket段
1. ListenStream： 监听指定的TCP端口或UNIX套接子文件
2. ListenDataGram：UDP端口
3. ListenSequentialPacket：UNIX套接子
4. ListenFIFO：管道文件
5. ListenMessageQueue：POSIX消息队列
6. ListenSpecial: 字符设备或特殊设备

####挂载点（.mount）
unit文件名需转译，‘ / ’ 转为 ‘ - ’ ， ‘  - ’转为 ‘ \x ’
例如 /media/my-mount     转译为 media-my\x2mount

	core@core-01 /usr $ systemd-escape media/my-mount  #去掉开头
	media-my\x2dmount

Mount 段
1. What: 被挂载设备绝对路径
2. Where：挂载点绝对目录，与文件名一致
3. Type：挂载文件系统类型
4. Options：挂载参数
5. SloppyOptions： true|false 是否忽略无法使别的挂载参数
6. DirectoryMode： 若指定目录不存在，则自动创建，权限为755
7. TimeoutSec，挂载超时秒数

####自动挂载文件系统 （.automount）

当用户访问某个目录时，自动将设定的文件系统挂载上去，与.mount 配合使用

Automount 段
1. Where: 挂载点的绝对路径，与文件名一致
2. DirectoryMode： 同Mount段
3. TimeoutIdleSec： 当挂载的目录在一定时间内没有使用，自动卸载


####交换分区(.swap)
命名规则同mount
Swap 段
1.What： 用于做交换分区的设备或路径
2.Priority: 若存在多个交换分区，选择优先级高的先使用
3. Options：参数
4. TimeoutSec: 挂载超时时间




####systemd-run
可将一个命令变成后台运行的服务，他的生命周期将由Systemd控制。不会因为启动他的控制台的关闭而关闭

	$ systemd-run  --uid=root --gid=root du -sh /*
	Running as unit run-rd72b6f65e0a84f8bad8408f33746bd62.service.


	



References:

[浅析 Linux 初始化 init 系统，第 3 部分: Systemd](http://www.ibm.com/developerworks/cn/linux/1407_liuming_init3/)
CoreOS 实践之路 林帆
