###CD_SERVICE IMAGE

考虑到potapi和cd_service之间有很多依赖重复，需要重新整理软件依赖结构。

1. 先将所有的安装写在一个Dockerfile里面，之后再找出相同的，整理依赖关系

2. cd_service image dockerfile

	
docker container 时钟同步问题  
http://dockone.io/question/505
-v /etc/localtime:/etc/localtime:ro



 LDAP的基本模型是建立在“条目”（Entry）的基础上。一个条目是一个或多个属性的集合，并且具有一个全局唯一的“可区分名称”（用dn表示 distinguished name）。
