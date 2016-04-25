##Marathon Event Bus


####
Marathon内部的事件总线捕获所有的API请求信息，订阅者可以通过marathon启动时配置或者启动后通过调用订阅API来向 event bus 注册。  
目前，marathon通过HTTP回调方式向所有订阅者发送json数据的POST请求。


配置

1.启动时配置

	$ ./bin/start --master ... --event_subscriber http_callback --http_endpoints http://host1/foo,http://host2/bar

2.发送请求，注册事件订阅

	curl -XPOST  http://marathon_host:port/v2/eventSubscriptions?callbackUrl=http://192.168.1.113:6080
	
	# marathon 运行在88的8080端口， 每当有事件触发，marathon都会向 host 192.168.1.89:34567/paas/callback 发送post请求 
	curl -XPOST "http://192.168.1.88:8080/v2/eventSubscriptions?callbackUrl=http://192.168.1.89:34567/paas/callback"



事件类型  

`api_post_event` :  每次marathon收到 app 操作请求（create，update,delete）都会触发该事件, json 数据如下 

	{
		"eventType": "api_post_event",
		"timestamp": "2014-03-01T23:29:30.158Z",
		"clientIp": "0:0:0:0:0:0:0:1",
		"uri": "/v2/apps/my-app",
		"appDefinition": {
			"args": [],
			"backoffFactor": 1.15,
			"backoffSeconds": 1,
			"cmd": "sleep 30",
			"constraints": [],
			"container": null,
			"cpus": 0.2,
			"dependencies": [],
			"disk": 0.0,
			"env": {},
			"executor": "",
			"healthChecks": [],
			"id": "/my-app",
			"instances": 2,
			"mem": 32.0,
			"ports": [10001],
			"requirePorts": false,
			"storeUrls": [],
			"upgradeStrategy": {
			"minimumHealthCapacity": 1.0
			},
			"uris": [],
			"user": null,
			"version": "2014-09-09T05:57:50.866Z"
		  }
	}


`status_update_event`


创建一个容器

	('eventType: ', u'api_post_event', 'timestamp: ', u'2016-04-24T09:27:47.044Z')
	192.168.1.88 - - [24/Apr/2016 17:30:52] "POST /paas/callback HTTP/1.1" 200 -
	('eventType: ', u'group_change_success', 'timestamp: ', u'2016-04-24T09:27:47.044Z')
	192.168.1.88 - - [24/Apr/2016 17:30:53] "POST /paas/callback HTTP/1.1" 200 -
	('eventType: ', u'deployment_step_success', 'timestamp: ', u'2016-04-24T09:27:47.047Z')
	192.168.1.88 - - [24/Apr/2016 17:30:53] "POST /paas/callback HTTP/1.1" 200 -
	('eventType: ', u'deployment_info', 'timestamp: ', u'2016-04-24T09:27:47.047Z')
	192.168.1.88 - - [24/Apr/2016 17:30:53] "POST /paas/callback HTTP/1.1" 200 -
	('eventType: ', u'deployment_info', 'timestamp: ', u'2016-04-24T09:27:47.046Z')
	192.168.1.88 - - [24/Apr/2016 17:30:53] "POST /paas/callback HTTP/1.1" 200 -
	('eventType: ', u'status_update_event', 'timestamp: ', u'2016-04-24T09:27:48.069Z')
	192.168.1.88 - - [24/Apr/2016 17:30:54] "POST /paas/callback HTTP/1.1" 200 -
	('eventType: ', u'deployment_step_success', 'timestamp: ', u'2016-04-24T09:27:48.078Z')
	192.168.1.88 - - [24/Apr/2016 17:30:54] "POST /paas/callback HTTP/1.1" 200 -
	('eventType: ', u'deployment_success', 'timestamp: ', u'2016-04-24T09:27:48.078Z')
	192.168.1.88 - - [24/Apr/2016 17:30:54] "POST /paas/callback HTTP/1.1" 200 -


删除


	('eventType: ', u'group_change_success', 'timestamp: ', u'2016-04-24T09:31:44.379Z')
	192.168.1.88 - - [24/Apr/2016 17:34:50] "POST /paas/callback HTTP/1.1" 200 -
	('eventType: ', u'deployment_info', 'timestamp: ', u'2016-04-24T09:31:44.390Z')
	192.168.1.88 - - [24/Apr/2016 17:34:50] "POST /paas/callback HTTP/1.1" 200 -
	('eventType: ', u'status_update_event', 'timestamp: ', u'2016-04-24T09:31:44.936Z')
	192.168.1.88 - - [24/Apr/2016 17:34:50] "POST /paas/callback HTTP/1.1" 200 -
	('eventType: ', u'app_terminated_event', 'timestamp: ', u'2016-04-24T09:31:44.941Z')
	192.168.1.88 - - [24/Apr/2016 17:34:50] "POST /paas/callback HTTP/1.1" 200 -
	('eventType: ', u'deployment_step_success', 'timestamp: ', u'2016-04-24T09:31:44.941Z')
	192.168.1.88 - - [24/Apr/2016 17:34:50] "POST /paas/callback HTTP/1.1" 200 -
	('eventType: ', u'deployment_success', 'timestamp: ', u'2016-04-24T09:31:44.941Z')
	192.168.1.88 - - [24/Apr/2016 17:34:50] "POST /paas/callback HTTP/1.1" 200 -