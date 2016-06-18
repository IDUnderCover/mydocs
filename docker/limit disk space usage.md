## Docker Container 磁盘使用限制


对docker 磁盘使用限额可以用 docker daemon 启动时参数 --storage-opt 设置，但这只支持device mapper的文件系统。
，我们也可以创建一个虚拟文件，将其挂载到docker的使用目录下。


1. 创建一个4G的虚拟文件

		razaura@ubuntu-home:~/dockerUsageLimit$ sudo dd if=/dev/zero  of=~/dockerUsageLimit/disk-quota.ext3 count=4096 bs=1M 
		记录了4096+0 的读入
		记录了4096+0 的写出
		4294967296 bytes (4.3 GB, 4.0 GiB) copied, 9.04433 s, 475 MB/s

		razaura@ubuntu-home:~/dockerUsageLimit$ ll -h
		总用量 4.1G
		drwxrwxr-x  2 razaura razaura 4.0K 6月  18 16:00 ./
		drwxr-xr-x 57 razaura razaura 4.0K 6月  18 15:59 ../
		-rw-r--r--  1 root    root    4.0G 6月  18 16:00 disk-quota.ext3

2. 在此磁盘文件上创建文件系统

		razaura@ubuntu-home:~/dockerUsageLimit$ sudo mkfs -t ext3 -F ./disk-quota.ext3
		mke2fs 1.42.13 (17-May-2015)
		Discarding device blocks: 完成                            
		Creating filesystem with 1048576 4k blocks and 262144 inodes
		Filesystem UUID: 4a41e634-d453-446b-833b-d02194c43390
		Superblock backups stored on blocks: 
		32768, 98304, 163840, 229376, 294912, 819200, 884736

		Allocating group tables: 完成                            
		正在写入inode表: 完成                            
		Creating journal (32768 blocks): 完成
		Writing superblocks and filesystem accounting information: 完成 		

3. 将该文件系统挂载到 `container` 的 `top layer` 即容器的读写层


		razaura@ubuntu-home:~/dockerUsageLimit$ docker run -ti --name=disktest alpine /bin/sh
		# 通过docker ps 获取到了容器ID 07f5e38f0c96
		# 该目录下可以查看到容器挂载层的ID
		root@ubuntu-home:/var/lib/docker/image/aufs/layerdb/mounts/07f5e38f0c964932b79f36d36935d4443430f74f700313747ad0a1550d4a1a42   ll
		总用量 20
		drwxr-xr-x 2 root root 4096 6月  18 16:24 ./
		drwxr-xr-x 9 root root 4096 6月  18 16:13 ../
		-rw-r--r-- 1 root root   69 6月  18 16:13 init-id     
		-rw-r--r-- 1 root root   64 6月  18 16:13 mount-id
		-rw-r--r-- 1 root root   71 6月  18 16:13 parent
		
		root@ubuntu-home:/var/lib/docker/image/aufs/layerdb/mounts/07f5e38f0c964932b79f36d36935d4443430f74f700313747ad0a1550d4a1a42 	cat mount-id 
		a8d1720c0bf0384c6549d8a31f6b147a71da72b507d0b62480b471cb5c176e28

		# 在/arfs/diff 下找到该目录，这就是此容器的top layer
		root@ubuntu-home:/var/lib/docker/aufs/diff/a8d1720c0bf0384c6549d8a31f6b147a71da72b507d0b62480b471cb5c176e28# ll
		总用量 16
		drwxr-xr-x  4 root root 4096 6月  18 16:13 ./
		drwx------ 31 root root 4096 6月  18 16:13 ../
		-r--r--r--  1 root root    0 6月  18 16:13 .wh..wh.aufs
		drwx------  2 root root 4096 6月  18 16:13 .wh..wh.orph/
		drwx------  2 root root 4096 6月  18 16:13 .wh..wh.plnk/

		# 在容器中执行以下命令创建一个文件，查看该文件是否出现在这目录下
		/ # touch hello
		/ # echo hello >> hello
		
		# 验证成功
		root@ubuntu-home:/var/lib/docker/aufs/diff/a8d1720c0bf0384c6549d8a31f6b147a71da72b507d0b62480b471cb5c176e28# ls -al
		总用量 24
		drwxr-xr-x  5 root root 4096 6月  18 16:31 ./
		drwx------ 31 root root 4096 6月  18 16:13 ../
		-rw-r--r--  1 root root    6 6月  18 16:31 hello
		drwx------  2 root root 4096 6月  18 16:31 root/
		-r--r--r--  1 root root    0 6月  18 16:13 .wh..wh.aufs
		drwx------  2 root root 4096 6月  18 16:13 .wh..wh.orph/
		drwx------  2 root root 4096 6月  18 16:13 .wh..wh.plnk/
		root@ubuntu-home:/var/lib/docker/aufs/diff/a8d1720c0bf0384c6549d8a31f6b147a71da72b507d0b62480b471cb5c176e28# cat hello 
		hello

		# 挂载刚才的文件系统到该目录
		razaura@ubuntu-home:~/dockerUsageLimit$ sudo mount -o loop,rw,usrquota,grpquota ./disk-quota.ext3 /var/lib/docker/aufs/diff/a8d1720c0bf0384c6549d8a31f6b147a71da72b507d0b62480b471cb5c176e28


目前失败了，容器还是使用了原来的磁盘空间 （docker version 1.11）

	Containers: 7
	 Running: 1
	 Paused: 0
	 Stopped: 6
	Images: 6
	Server Version: 1.11.2
	Storage Driver: aufs
	 Root Dir: /var/lib/docker/aufs
	 Backing Filesystem: extfs
	 Dirs: 29
	 Dirperm1 Supported: true
	Logging Driver: json-file
	Cgroup Driver: cgroupfs
	Plugins: 
	 Volume: local
	 Network: host bridge null
	Kernel Version: 4.4.0-24-generic
	Operating System: Ubuntu 16.04 LTS
	OSType: linux
	Architecture: x86_64
	CPUs: 4
	Total Memory: 7.732 GiB
	Name: ubuntu-home
	ID: IUSY:GUA7:QD6L:4FML:LADX:U6RZ:GMTR:HYQA:7OHY:54YM:LJH7:6TK7
	Docker Root Dir: /var/lib/docker
	Debug mode (client): false
	Debug mode (server): false
	Registry: https://index.docker.io/v1/
	WARNING: No swap limit support
