##Control Group

CGroup 可用来控制进程的资源使用限制

CGroup 主要有三个概念

1. 层级
	层级指一组 CGroup 配置数，他包含多个子系统
2. 子系统
	一种子系统对应一种资源限制，子系统下包含多个控制组
3. 控制组
	控制组即为一组所受子系统限制的进程组


例子：

创建一个层级
	
	# 创建一个目录
	$ mkdir cgroup
	# 将 cgroup_root 根设备挂载到该目录下
	$ mount -t tmpfs cgroup_root cgroup
	# 一个层级就创建好了

在层级创建一个子系统
	
	
	$ cd cgroup
	$ mkdir cpu
	# 挂载cpu子系统
	$ mount -t cgroup -o cpu cgroup cpu
	

在子系统内创建控制组

	# 创建完后，目录下会多许多文件
	$ mkdir myset
	
	限制某进程的cpu使用率
	$ echo 30000 > cpu.cfs_tuota_us  # 30% cpu
	$ echo $PID > tasks   # 将PID进程cpu使用限制为30% 