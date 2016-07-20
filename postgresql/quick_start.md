PostgreSQL

安装
	
	sudo apt-get install postgresql

添加新用户和数据库

	#创建一个新的Linux用户
	sudo adduser dbuser
	
	#切换到postgres用户
	sudo su - postgres

	#使用psql登录控制台，相当于使用系统用户postgres同名的数据库用户身份
	psql
	
	为postgres用户设置密码
	postgres=# \password postgres

	创建数据库用户 dbuser
	CREATE USER dbuser WITH PASSWORD 'password' ;

	创建用户数据库, 并指定所有者为dbuser
	 CREATE DATABASE lagoudb OWNER dbuser ;

	将lagoudb的所有权限赋予给dbuser
	postgres-# grant all privileges on database lagoudb to dbuser

	# 退出
	postgres-# \q

	# 在bash shell 里用该命令登录数据库
	psql -U dbuser -d lagoudb -h localhost -p 5432

json 操作

json 和 jsonb的区别

There are two JSON data types: json and jsonb. They accept almost identical sets of values as input. The major practical difference is one of efficiency. The json data type stores an exact copy of the input text, which processing functions must reparse on each execution; while jsonb data is stored in a decomposed binary format that makes it slightly slower to input due to added conversion overhead, but significantly faster to process, since no reparsing is needed. jsonb also supports indexing, which can be a significant advantage.

如果没有特殊需求，比如需要保持键的顺序，一般我们都使用`jsonb`




python 接口需要安装

	sudo apt-get install python-psycopg2
	sudo apt-get install libpq-dev


命令行参考

\d  + 数据库名 查看所有表
\d + 表名 查看表结构


参考：
	http://www.ruanyifeng.com/blog/2013/12/getting_started_with_postgresql.html  
	https://segmentfault.com/a/1190000002911580  
	https://www.postgresql.org/docs/9.4/static/datatype-json.html
	
