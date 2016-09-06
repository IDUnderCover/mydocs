##ANSIBLE

###Basic
Ansible manages machines over the SSH protocol

	$ git clone git://github.com/ansible/ansible.git --recursive
	$ cd ./ansible
	$ source ./hacking/env-setup
	$ sudo pip install paramiko PyYAML Jinja2 httplib2 six
	$ echo "127.0.0.1" > ~/ansible_hosts
	$ export ANSIBLE_INVENTORY=~/ansible_hosts
	$ ansible all -m ping --ask-pass	


if password is required, supply hte option `--ask-pass` 


edit the [Inventory](/ansible/intro_inventory.html) (saved in /etc/ansible/hosts by default)

Run a command on all of your nodes

	ansible all -a "/bin/echo hello"


###Inventory

	mail.example.com
	
	[webservers] # group name
	foo.example.com
	bar.example.com
	
	[dbservers]
	one.example.com
	two.example.com
	three.example.com

Group Variables

	[atlanta]
	host1
	[atlanta:vars]
	ntp_server=ntp.atlanta.example.com

Groups of Groups, and Group Variables
 
	[usa:children] 
	southeast
	northeast
	southwest
	northwest

the suffix :vars for variables and :children for subgroups




###Non-SSH connections types

docker 


### Pattern
A pattern usually refers to a set of groups, which are sets of hosts definded in your inventory.

	all is equal to *

	pattern address can be one or more groups
	websevers:dbservers   # or
	webserver:&dbservers  # both in web and dbservers
	webserver:!dbservers  # in web ,not in dbservers


### Ad-Hoc Commands


### playbook basic


	---
	- hosts: webservers # groups or host patterns
	  remote_user: root  # user account
	  tasks:
	    - name: test connection
	      ping:
          remote_user: name


Each play contains a list of tasks. Tasks are executed in order, one at a time, against all machines matched by the host pattern, before moving on to the next task. 


Reference:
[Ansible Docs](http://docs.ansible.com/ansible/)


####Directory Layout

	production                # inventory file for production servers
	staging                   # inventory file for staging environment
	
	group_vars/
	   group1                 # here we assign variables to particular groups
	   group2                 # ""
	host_vars/
	   hostname1              # if systems need specific variables, put them here
	   hostname2              # ""
	
	library/                  # if any custom modules, put them here (optional)
	filter_plugins/           # if any custom filter plugins, put them here (optional)
	
	site.yml                  # master playbook
	webservers.yml            # playbook for webserver tier
	dbservers.yml             # playbook for dbserver tier
	
	roles/
	    common/               # this hierarchy represents a "role"
	        tasks/            #
	            main.yml      #  <-- tasks file can include smaller files if warranted
	        handlers/         #
	            main.yml      #  <-- handlers file
	        templates/        #  <-- files for use with the template resource
	            ntp.conf.j2   #  <------- templates end in .j2
	        files/            #
	            bar.txt       #  <-- files for use with the copy resource
	            foo.sh        #  <-- script files for use with the script resource
	        vars/             #
	            main.yml      #  <-- variables associated with this role
	        defaults/         #
	            main.yml      #  <-- default lower priority variables for this role
	        meta/             #
	            main.yml      #  <-- role dependencies
	
	    webtier/              # same kind of structure as "common" was above, done for the webtier role
	    monitoring/           # ""
	    fooapp/               # ""


debconf  
debconf-set-selections  
https://en.wikipedia.org/wiki/Debconf_(software_package)
http://docs.ansible.com/ansible/debconf_module.html  
https://serversforhackers.com/video/installing-mysql-with-debconf  

Docker Module  
http://docs.ansible.com/ansible/docker_module.html


Error 0

	TASK [shendahui.ldap_role : Run openldap container] ****************************
	fatal: [test]: FAILED! => {"changed": false, "failed": true, "msg": "`docker-py` doesn't seem to be installed, but is required for the Ansible Docker module."}

Solution
 
	vim shendahui.python_init_role/vars/trusty.yml 
	add docker-py



Error 1

	TASK [gitlab_role : Generate gitlab configuration file.] ***********************
	fatal: [test]: FAILED! => {"changed": true, "failed": true, "msg": "Destination directory /etc/gitlab does not exist"}
	
Solution

	create the directory



Error 2

	TASK [gitlab_role : Add user www-data to group gitlab-www] *********************
	fatal: [test]: FAILED! => {"changed": false, "failed": true, "msg": "Group gitlab-www does not exist"}

Solution 
	
	 这是gitlab在使用外部nginx时需要配置的东西，注释掉以下几行即可
	
	# - name: Add user www-data to group gitlab-www
	#   user: name=www-data group=gitlab-www append=yes


Error 3

	TASK [devpi_role : run a devpi container] **************************************
	fatal: [test]: FAILED! => {"changed": false, "changes": ["{\"status\":\"Pulling repository mirrors.shatacloud.com/shata/devpi\"}\r\n", "{\"errorDetail\":{\"message\":\"Error: image shata/devpi:latest not found\"},\"error\":\"Error: image shata/devpi:latest not found\"}\r\n"], "failed": true, "msg": "Unrecognized status from pull.", "status": ""}

Solution

	在 docker 启动时指定了 force pull，而在测试时无法连接shatacloud，所以会报错



Error 4 

	shata@ubuntu:~$ docker logs potapi
	Log init successfully, logs output to /opt/devenv/logs/sys_execute.log
	initial git handler failed: HTTPConnectionPool(host='scm.example.com', port=80): Max retries exceeded with url: /api/v3/session (Caused by NewConnectionError('<requests.packages.urllib3.connection.HTTPConnection object at 0x7fa713090990>: Failed to establish a new connection: [Errno 111] Connection refused',))

Solution

	临时解决方案，修改主机host 文件，将 *.example.com 127.0.0.1


Error 5

	potfront nginx 配置反代 端口错误
	写死 修改为 28080


Error 6

	shata@ubuntu:~$ docker logs da3eb2a5c421
	 init successfully, logs output to /opt/devenv/logs/sys_execute.log
	current gitlab user: Administrator
	Traceback (most recent call last):
  	File "/usr/local/bin/pot-api", line 7, in <module>
	    run()
	  File "/usr/local/lib/python2.7/site-packages/potapi/__init__.py", line 43, in run
	    from potapi import event_function
	  File "/usr/local/lib/python2.7/site-packages/potapi/event_function.py", line 8, in <module>
	    from potapi.modules import GroupModule
	  File "/usr/local/lib/python2.7/site-packages/potapi/modules.py", line 16, in <module>
	    import utils.temp
	  File "/usr/local/lib/python2.7/site-packages/potapi/utils/temp.py", line 4, in <module>
	    from potapi.utils.handlers import gitlab_handler, jenkins_handler
	  File "/usr/local/lib/python2.7/site-packages/potapi/utils/handlers/__init__.py", line 30, in <module>
	    jenkins_config['PASSWORD'])
	  File "/usr/local/lib/python2.7/site-packages/potapi/utils/handlers/pot_jenkins.py", line 20, in __init__
	    self.git_plugin_info = self.get_plugin_info('git')
	  File "/usr/local/lib/python2.7/site-packages/jenkins/__init__.py", line 678, in get_plugin_info
	    plugins_info = self.get_plugins(depth)
	  File "/usr/local/lib/python2.7/site-packages/jenkins/__init__.py", line 719, in get_plugins
	    % self.server)
	jenkins.BadHTTPException: Error communicating with server[http://ci.example.com:80/]



### variables
