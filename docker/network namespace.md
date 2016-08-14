创建一个测试network namespace

	sudo ip netns add  nstest

创建一对虚拟网卡  

	sudo ip link add veth-a type veth peer name veth-b

将 veth-a 留在主机中, veth-b 放入 nstest 中

	sudo ip link set veth-b netns nstest


