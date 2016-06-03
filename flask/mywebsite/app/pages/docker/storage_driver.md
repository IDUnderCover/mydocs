title: Docker Daemnon Storage Driver
date: 2016-05-24
tags: [docker, Storage Driver]


## Docker Daemnon Storage Driver
这文章主要介绍 docker daemon 的几个存储驱动，OverlayFS，AUFS，Btrfs，Device Mapper，VFS，ZFS。

先从 docker hub 上拉取以下两个镜像，准备一个干净的测试环境

    docker pull docker:dind
	docker pull docker:1.11


###[AUFS](http://aufs.sourceforge.net/)
AUFS是一种联合挂载技术，将几个目录挂载到同一目录下，提供给用户一个统一的整体视图。
它是 docker 采用的第一个存储驱动，它有以下几个优点

- Fast container startup times
- Efficient use of storage
- Efficient use of memory (linux page cache)

但是由于它不包含在linux kernel mainline，所以有的linux发行版本不支持AUFS，下面举个简单的aufs使用例子来增强对其的理解。

	# create three directories
    $ mkdir /tmp/dir{1,2} /tmp/aufs 
	
	# touch two files in dir1 and dir2
	$ touch /tmp/dir1/file1 /tmp/dir2/file2
 
	# mount dir1 and dir2 on aufs
	$ mount -t aufs -o br=/tmp/dir1:/tmp/dir2 none /tmp/aufs

	# then you can see file1 and file2 in /tmp/aufs
	$　ls /tmp/aufs
	   file1  file2


####docker 镜像在aufs文件系统下的组织形式

![aufs_layers.jpg](http://i.imgur.com/cX77rsj.jpg)

从这张图中可以看出，每一个image layer 和 container layer 都对应着一个目录，通过最终的union mount 构造出所有layers的整体视图。

如果需要读取一个文件时，会从container layer 开始依次向下寻找该文件，直到找到该文件并打开它，镜像堆叠层数越多，搜索的目录树深度越大。

编辑一个文件时，会按上述方法先找到该文件，然后在将其拷贝到读写层进行修改（Copy on Write，COW），但如果文件很大，即使只有文件的小部分需要改动，也会将整个文件拷贝，这对性能有很大的影响。

删除文件只是在 top layer 增加一个 whiteout file 来隐蔽该文件的存在性。
 
![aufs_delete.jpg](http://i.imgur.com/GOyv6ya.jpg)


####以aufs为存储驱动启动docker daemon

启动 docker daemon 

	# start docker daemon with AUFS
	$ docker run -d -ti --privileged --name=docker-daemon docker:dind -s aufs
	124115d87c44d74492ca3197e847773adc234775a410fa25685fea4237c2dd5a


查看docker-daemon 的启动日志，graphdriver为aufs	

	$ docker logs docker-daemon
	WARN[0000] /!\ DON'T BIND ON ANY IP ADDRESS WITHOUT setting -tlsverify IF YOU DON'T KNOW WHAT YOU'RE DOING /!\ 
	INFO[0000] New containerd process, pid: 30
	             
	INFO[0001] Graph migration to content-addressability took 0.00 seconds 
	WARN[0001] Running modprobe bridge br_netfilter failed with message: modprobe: can't change directory to '/lib/modules': No such file or directory
	, error: exit status 1 
	WARN[0001] Running modprobe nf_nat failed with message: `modprobe: can't change directory to '/lib/modules': No such file or directory`, error: exit status 1 
	WARN[0001] Running modprobe xt_conntrack failed with message: `modprobe: can't change directory to '/lib/modules': No such file or directory`, error: exit status 1 
	INFO[0001] Default bridge (docker0) is assigned with an IP address 172.18.0.0/16. Daemon option --bip can be used to set a preferred IP address 
	WARN[0001] Your kernel does not support swap memory limit. 
	WARN[0001] mountpoint for pids not found                
	INFO[0001] Loading containers: start.                   
	
	INFO[0001] Loading containers: done.                    
	INFO[0001] Daemon has completed initialization          
	INFO[0001] Docker daemon                                 commit=4dc5990 graphdriver=aufs version=1.11.0
	INFO[0001] API listen on [::]:2375                      
	INFO[0001] API listen on /var/run/docker.sock  

拉取 busybox 镜像

	# pull busybox image 
	$ docker run --rm -ti --link docker-daemon:docker docker:1.11  docker pull busybox
	Using default tag: latest
	latest: Pulling from library/busybox
	385e281300cc: Pull complete 
	a3ed95caeb02: Pull complete 
	Digest: sha256:4a887a2326ec9e0fa90cce7b4764b0e627b5d6afcb81a3f73c85dc29cea00048
	Status: Downloaded newer image for busybox:latest


查看 docker info

	$ docker run --rm -ti --link docker-daemon:docker docker:1.11  docker info         
	Containers: 0
     Running: 0
     Paused: 0
     Stopped: 0
    Images: 1
    Server Version: 1.11.0
    Storage Driver: aufs
     Root Dir: /var/lib/docker/aufs
     Backing Filesystem: extfs
     Dirs: 2
     Dirperm1 Supported: true
    Logging Driver: json-file
    Cgroup Driver: cgroupfs
    Plugins: 
     Volume: local
     Network: null host bridge
    Kernel Version: 3.16.0-67-generic
    Operating System: Alpine Linux v3.3 (containerized)
    OSType: linux
    Architecture: x86_64
    CPUs: 16
    Total Memory: 62.91 GiB
    Name: 124115d87c44
    ID: VCSZ:JFSY:RLNM:TLTP:ODSS:NJBT:6ZTQ:DK5H:2HB4:ZWGI:7ZE2:PUK4
    Docker Root Dir: /var/lib/docker
    Debug mode (client): false
    Debug mode (server): false
    Registry: https://index.docker.io/v1/
    WARNING: No swap limit support
    WARNING: bridge-nf-call-iptables is disabled
    WARNING: bridge-nf-call-ip6tables is disabled


进入docker-daemon 查看镜像存储的目录结构

	$ docker exec -ti docker-daemon /bin/sh		
	/ # cd /var/lib/docker
	
	/var/lib/docker # ls
	aufs        containers  image       network     tmp         trust       volumes

	/var/lib/docker # ls aufs
	diff    layers  mnt

在拉取busybox镜像前，三个目录 `diff layers mnt`下内容都为空，busybox 镜像有两层layer，每层layer的创建都涉及以下过程

-  在 `diff` 和 `mnt` 创建与 `layer id` 同名的文件夹， 在 `layers`目录下创建与其 `layer id` 同名的文件，里面写入其所依赖的 `paraent layers ids`
-  将系统文件内容存放 `diff/layerid` 目录下
   
用 `docker hostory busybox ` 命令查看 busybox 镜像的历史构建信息

	$ docker history busybox	
	IMAGE               CREATED             CREATED BY                                      SIZE                COMMENT
	47bcc53f74dc        4 weeks ago         /bin/sh -c #(nop) CMD ["sh"]                    0 B                 
	<missing>           4 weeks ago         /bin/sh -c #(nop) ADD file:47ca6e777c36a4cfff   1.113 MB            


查看 diff 目录下的文件内容

	/var/lib/docker/aufs # tree diff -L 2
    diff
	├── 5d8bd832e5b57b4bcae47147825941d908776ab10d02d1f6ef709b503050772b
	│   ├── bin
	│   ├── dev
	│   ├── etc
	│   ├── home
	│   ├── root
	│   ├── tmp
	│   ├── usr
	│   └── var
	└── 6f8bb4608530aca65035743db8552262a394ffe7c0c5fa1b63ab9a3291db77a5

发现 `6f8bb4` 目录下并没有内容，因为最后一层的layer的创建只是执行 `CMD ["sh"]` 并没有产生实际内容

接下来运行 busybox 容器
	
	/var/lib/docker/aufs # docker run -tid busybox 
	ab2f60b333c8b57fccb58cacfe36811a592db440dbdb1b06bb60c64f9aefd741


观察这三个目录内容变化情况，发现都创建了两个新的目录，719da24 和 719da24-init
	
	/var/lib/docker/aufs # tree . -L 2
	.
	├── diff
	│   ├── 5d8bd832e5b57b4bcae47147825941d908776ab10d02d1f6ef709b503050772b
	│   ├── 6f8bb4608530aca65035743db8552262a394ffe7c0c5fa1b63ab9a3291db77a5
	│   ├── 719da241fb9834d3f4b517515c51883f622811516335c47b5b15b256d455b881
	│   └── 719da241fb9834d3f4b517515c51883f622811516335c47b5b15b256d455b881-init
	├── layers
	│   ├── 5d8bd832e5b57b4bcae47147825941d908776ab10d02d1f6ef709b503050772b
	│   ├── 6f8bb4608530aca65035743db8552262a394ffe7c0c5fa1b63ab9a3291db77a5
	│   ├── 719da241fb9834d3f4b517515c51883f622811516335c47b5b15b256d455b881
	│   └── 719da241fb9834d3f4b517515c51883f622811516335c47b5b15b256d455b881-init
	└── mnt
	    ├── 5d8bd832e5b57b4bcae47147825941d908776ab10d02d1f6ef709b503050772b
	    ├── 6f8bb4608530aca65035743db8552262a394ffe7c0c5fa1b63ab9a3291db77a5
	    ├── 719da241fb9834d3f4b517515c51883f622811516335c47b5b15b256d455b881
	    └── 719da241fb9834d3f4b517515c51883f622811516335c47b5b15b256d455b881-init

`719da-init` 下的文件许多都在容器运行时决定，例如 `resolv.conf` 会根据DNS配置来生成相应的内容。所以这不部分文件不适合放在镜像文件里。

	/var/lib/docker/aufs/diff # tree 719da241fb9834d3f4b517515c51883f622811516335c47b5b15b256d455b881-init/ -L 2
	719da241fb9834d3f4b517515c51883f622811516335c47b5b15b256d455b881-init/
	├── dev
	│   ├── console
	│   ├── pts
	│   └── shm
	├── etc
	│   ├── hostname
	│   ├── hosts
	│   ├── mtab -> /proc/mounts
	│   └── resolv.conf
	├── proc
	└── sys

`719da` 目录是新建的读写目录，所有对该容器的读写都会写入到该文件夹。 从 `layers` 目录文件下的信息也很容易发现，`719da` 是该容器的 `top layer`, 它依赖于以下三个`layers`


	/var/lib/docker/aufs # cat layers/719da241fb9834d3f4b517515c51883f622811516335c47b5b15b256d455b881
	719da241fb9834d3f4b517515c51883f622811516335c47b5b15b256d455b881-init
	6f8bb4608530aca65035743db8552262a394ffe7c0c5fa1b63ab9a3291db77a5
	5d8bd832e5b57b4bcae47147825941d908776ab10d02d1f6ef709b503050772b
	/var/lib/docker/aufs # cat layers/719da241fb9834d3f4b517515c51883f622811516335c47b5b15b256d455b881-init 
	6f8bb4608530aca65035743db8552262a394ffe7c0c5fa1b63ab9a3291db77a5
	5d8bd832e5b57b4bcae47147825941d908776ab10d02d1f6ef709b503050772b


最后 `diff` 下的该镜像的相关目录都 `union mount` 到了 `mnt/719da241fb9834d3f4b517515c51883f622811516335c47b5b15b256d455b881`

	/var/lib/docker/aufs # tree mnt/ -L 2
	mnt/
	├── 5d8bd832e5b57b4bcae47147825941d908776ab10d02d1f6ef709b503050772b
	├── 6f8bb4608530aca65035743db8552262a394ffe7c0c5fa1b63ab9a3291db77a5
	├── 719da241fb9834d3f4b517515c51883f622811516335c47b5b15b256d455b881
	│   ├── bin
	│   ├── dev
	│   ├── etc
	│   ├── home
	│   ├── proc
	│   ├── root
	│   ├── sys
	│   ├── tmp
	│   ├── usr
	│   └── var
	└── 719da241fb9834d3f4b517515c51883f622811516335c47b5b15b256d455b881-init

如果将容器停止，那么 `mnt/719da241fb9834d3f4b517515c51883f622811516335c47b5b15b256d455b881` 会被 unmount，但对该容器写入的内容会保存在 `diff/719da241fb9834d3f4b517515c51883f622811516335c47b5b15b256d455b881` 目录下，下次启动该容器，内容又会复原。

	/var/lib/docker/aufs # tree mnt/ -L 2
	mnt/
	├── 5d8bd832e5b57b4bcae47147825941d908776ab10d02d1f6ef709b503050772b
	├── 6f8bb4608530aca65035743db8552262a394ffe7c0c5fa1b63ab9a3291db77a5
	├── 719da241fb9834d3f4b517515c51883f622811516335c47b5b15b256d455b881
	└── 719da241fb9834d3f4b517515c51883f622811516335c47b5b15b256d455b881-init
	
	4 directories, 0 files


###[Device Mapper]()
###[Btrfs]()
###[OverlayFS]()




###References:  
*Docker 容器与容器云 3.6节 Docker的存储驱动*   
[AUFS](http://aufs.sourceforge.net/)  
[ChinaUnix aufs 中文资料](http://bbs.chinaunix.net/thread-1958383-1-1.html)   
[Docker in Docker](https://hub.docker.com/_/docker/)  
[Docker and AUFS in practice](https://docs.docker.com/engine/userguide/storagedriver/aufs-driver/)  
