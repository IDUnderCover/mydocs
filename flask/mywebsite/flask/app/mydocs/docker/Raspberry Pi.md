## Docker on Raspberry Pi


###系统安装

参考该 [wiki](https://archlinuxarm.org/platforms/armv7/broadcom/raspberry-pi-2)  

需要注意树莓派的版本

###  install docker


	
	国内镜像换源 在 /etc/pacman.d/mirrolist 中添加该行
	Server = http://mirrors.ustc.edu.cn/archlinuxarm/$arch/$repo

	更新系统
	[root@alarmpi alarm]# pacman -Syu

	重启机器
	[root@alarmpi alarm]# reboot

	安装 docker
	[root@alarmpi alarm]# pacman -S docker

	启动docker
	[root@alarmpi alarm]# system start docker

	查看docker 信息
	[root@alarmpi alarm]# docker info
	Containers: 0
	 Running: 0
	 Paused: 0
	 Stopped: 0
	Images: 0
	Server Version: 1.11.1
	Storage Driver: aufs
	 Root Dir: /var/lib/docker/aufs
	 Backing Filesystem: extfs
	 Dirs: 0
	 Dirperm1 Supported: true
	Logging Driver: json-file
	Cgroup Driver: cgroupfs
	Plugins: 
	 Volume: local
	 Network: host bridge null
	Kernel Version: 4.4.8-2-ARCH
	Operating System: Arch Linux ARM
	OSType: linux
	Architecture: armv7l
	CPUs: 4
	Total Memory: 922.3 MiB
	Name: alarmpi
	ID: U3EQ:Q4EH:WA63:3ZIK:Z5NR:PYJR:D7ID:XRCJ:552Z:T4NC:NTCE:SVCJ
	Docker Root Dir: /var/lib/docker
	Debug mode (client): false
	Debug mode (server): false
	Registry: https://index.docker.io/v1/
	WARNING: No cpuset support


	设置开机自启动
	[root@alarmpi alarm]# systemctl enable docker