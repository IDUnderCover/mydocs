##tmux & vim


会话

tmux new-session -s name [init_command]

关闭一个会话
tmux kill-session -t htop

prefix + :  进入命令行

[detach]
prefix + d

[attach]
tmux attch -t <target-session>

输出所有session
prefix + : + ls  

一个会话有多个window

创建新的窗口
prefix + c
窗口列表
prefix + w
切换窗口
prefix + p/n/[0-9]
更改窗口名称
prefix + ,
关闭窗口
prefix + &



切分窗格
左右切分
prefix + %
垂直切分
prefix + "

配置文件
~/.tmux.conf
	
	# set new prefix
	set -g prefix C-a
	# unbind old prefix
	unbind C-b
	
	# pane selection
	bind-key k select-pane -U
	bind-key j select-pane -D
	bind-key h select-pane -L
	bind-key l select-pane -R




 
