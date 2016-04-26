##Marathon Event Bus



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




---

删除1

		('eventType: ', u'group_change_success', 'timestamp: ', u'2016-04-26T09:04:20.782Z')
		192.168.1.88 - - [26/Apr/2016 17:05:43] "POST /paas/callback HTTP/1.1" 200 -

		('eventType: ', u'deployment_info', 'timestamp: ', u'2016-04-26T09:04:20.782Z')
		('step:', {u'actions': [{u'app': u'/11/d299fc210b8d11e68d2e005056c00008', u'type': u'StopApplication'}]})
		('action:', u'actions')
		192.168.1.88 - - [26/Apr/2016 17:05:43] "POST /paas/callback HTTP/1.1" 200 -

		('eventType: ', u'status_update_event', 'timestamp: ', u'2016-04-26T09:04:21.276Z')
		('status', {u'ipAddresses': [], u'timestamp': u'2016-04-26T09:04:21.276Z', u'eventType': u'status_update_event', u'taskStatus': u'TASK_KILLED', u'host': u'ubuntuServer', u'version': u'2016-04-26T09:00:57.497Z', u'taskId': u'11_d299fc210b8d11e68d2e005056c00008.63e2c937-0b8d-11e6-93fa-1e9f5e84c2a3', u'appId': u'/11/d299fc210b8d11e68d2e005056c00008', u'message': u'', u'slaveId': u'bc989b76-a481-4b88-a806-0c0bf770a738-S1', u'ports': [31311]})
		192.168.1.88 - - [26/Apr/2016 17:05:44] "POST /paas/callback HTTP/1.1" 200 -

		('eventType: ', u'app_terminated_event', 'timestamp: ', u'2016-04-26T09:04:21.281Z')
		192.168.1.88 - - [26/Apr/2016 17:05:44] "POST /paas/callback HTTP/1.1" 200 -

		('eventType: ', u'deployment_success', 'timestamp: ', u'2016-04-26T09:04:21.282Z')
		192.168.1.88 - - [26/Apr/2016 17:05:44] "POST /paas/callback HTTP/1.1" 200 -

		('eventType: ', u'deployment_step_success', 'timestamp: ', u'2016-04-26T09:04:21.282Z')
		192.168.1.88 - - [26/Apr/2016 17:05:44] "POST /paas/callback HTTP/1.1" 200 -



删除2
		('eventType: ', u'group_change_success', 'timestamp: ', u'2016-04-26T09:19:53.610Z')
		192.168.1.88 - - [26/Apr/2016 17:21:16] "POST /paas/callback HTTP/1.1" 200 -
		('eventType: ', u'deployment_info', 'timestamp: ', u'2016-04-26T09:19:53.615Z')
		('deployment_id:', u'64da4d37-c9db-4a61-ae41-9cb699021669')
		('step:', {u'actions': [{u'app': u'/11/f5d6b7910b8e11e6955d005056c00008', u'type': u'StopApplication'}]})
		('action:', u'actions')
		192.168.1.88 - - [26/Apr/2016 17:21:16] "POST /paas/callback HTTP/1.1" 200 -
		('eventType: ', u'status_update_event', 'timestamp: ', u'2016-04-26T09:19:54.138Z')
		('status', {u'ipAddresses': [], u'timestamp': u'2016-04-26T09:19:54.138Z', u'eventType': u'status_update_event', u'taskStatus': u'TASK_KILLED', u'host': u'ubuntuServer', u'version': u'2016-04-26T09:09:06.081Z', u'taskId': u'11_f5d6b7910b8e11e6955d005056c00008.871bdb2a-0b8e-11e6-93fa-1e9f5e84c2a3', u'appId': u'/11/f5d6b7910b8e11e6955d005056c00008', u'message': u'', u'slaveId': u'bc989b76-a481-4b88-a806-0c0bf770a738-S1', u'ports': [31150]})
		192.168.1.88 - - [26/Apr/2016 17:21:17] "POST /paas/callback HTTP/1.1" 200 -
		('eventType: ', u'app_terminated_event', 'timestamp: ', u'2016-04-26T09:19:54.143Z')
		192.168.1.88 - - [26/Apr/2016 17:21:17] "POST /paas/callback HTTP/1.1" 200 -
		('eventType: ', u'deployment_step_success', 'timestamp: ', u'2016-04-26T09:19:54.143Z')
		192.168.1.88 - - [26/Apr/2016 17:21:17] "POST /paas/callback HTTP/1.1" 200 -
		('eventType: ', u'deployment_success', 'timestamp: ', u'2016-04-26T09:19:54.143Z')
		192.168.1.88 - - [26/Apr/2016 17:21:17] "POST /paas/callback HTTP/1.1" 200 -




创建1

		('eventType: ', u'group_change_success', 'timestamp: ', u'2016-04-26T09:09:06.129Z')
		192.168.1.88 - - [26/Apr/2016 17:10:29] "POST /paas/callback HTTP/1.1" 200 -

		('eventType: ', u'api_post_event', 'timestamp: ', u'2016-04-26T09:09:06.129Z')
		192.168.1.88 - - [26/Apr/2016 17:10:29] "POST /paas/callback HTTP/1.1" 200 -

		('eventType: ', u'deployment_info', 'timestamp: ', u'2016-04-26T09:09:06.129Z')
		('step:', {u'actions': [{u'app': u'/11/f5d6b7910b8e11e6955d005056c00008', u'type': u'StartApplication'}]})
		('step:', {u'actions': [{u'app': u'/11/f5d6b7910b8e11e6955d005056c00008', u'type': u'ScaleApplication'}]})
		('action:', u'actions')
		192.168.1.88 - - [26/Apr/2016 17:10:29] "POST /paas/callback HTTP/1.1" 200 -

		('eventType: ', u'deployment_info', 'timestamp: ', u'2016-04-26T09:09:06.131Z')
		('step:', {u'actions': [{u'app': u'/11/f5d6b7910b8e11e6955d005056c00008', u'type': u'StartApplication'}]})
		('step:', {u'actions': [{u'app': u'/11/f5d6b7910b8e11e6955d005056c00008', u'type': u'ScaleApplication'}]})
		('action:', u'actions')
		192.168.1.88 - - [26/Apr/2016 17:10:29] "POST /paas/callback HTTP/1.1" 200 -

		('eventType: ', u'deployment_step_success', 'timestamp: ', u'2016-04-26T09:09:06.131Z')
		192.168.1.88 - - [26/Apr/2016 17:10:29] "POST /paas/callback HTTP/1.1" 200 -

		('eventType: ', u'status_update_event', 'timestamp: ', u'2016-04-26T09:09:07.085Z')
		('status', {u'ipAddresses': [], u'timestamp': u'2016-04-26T09:09:07.085Z', u'eventType': u'status_update_event', u'taskStatus': u'TASK_RUNNING', u'host': u'ubuntuServer', u'version': u'2016-04-26T09:09:06.081Z', u'taskId': u'11_f5d6b7910b8e11e6955d005056c00008.871bdb2a-0b8e-11e6-93fa-1e9f5e84c2a3', u'appId': u'/11/f5d6b7910b8e11e6955d005056c00008', u'message': u'', u'slaveId': u'bc989b76-a481-4b88-a806-0c0bf770a738-S1', u'ports': [31150]})
		192.168.1.88 - - [26/Apr/2016 17:10:30] "POST /paas/callback HTTP/1.1" 200 -

		('eventType: ', u'deployment_success', 'timestamp: ', u'2016-04-26T09:09:07.097Z')
		192.168.1.88 - - [26/Apr/2016 17:10:30] "POST /paas/callback HTTP/1.1" 200 -

		('eventType: ', u'deployment_step_success', 'timestamp: ', u'2016-04-26T09:09:07.097Z')
		192.168.1.88 - - [26/Apr/2016 17:10:30] "POST /paas/callback HTTP/1.1" 200 -



创建2

		('eventType: ', u'group_change_success', 'timestamp: ', u'2016-04-26T09:20:26.547Z')
		192.168.1.88 - - [26/Apr/2016 17:21:49] "POST /paas/callback HTTP/1.1" 200 -
		('eventType: ', u'api_post_event', 'timestamp: ', u'2016-04-26T09:20:26.547Z')
		192.168.1.88 - - [26/Apr/2016 17:21:49] "POST /paas/callback HTTP/1.1" 200 -
		('eventType: ', u'deployment_info', 'timestamp: ', u'2016-04-26T09:20:26.548Z')
		('deployment_id:', u'12366297-449c-44af-815c-b0de042c6da2')
		('step:', {u'actions': [{u'app': u'/11/8b6755210b9011e68400005056c00008', u'type': u'StartApplication'}]})
		('step:', {u'actions': [{u'app': u'/11/8b6755210b9011e68400005056c00008', u'type': u'ScaleApplication'}]})
		('action:', u'actions')
		192.168.1.88 - - [26/Apr/2016 17:21:49] "POST /paas/callback HTTP/1.1" 200 -
		('eventType: ', u'deployment_info', 'timestamp: ', u'2016-04-26T09:20:26.547Z')
		('deployment_id:', u'12366297-449c-44af-815c-b0de042c6da2')
		('step:', {u'actions': [{u'app': u'/11/8b6755210b9011e68400005056c00008', u'type': u'StartApplication'}]})
		('step:', {u'actions': [{u'app': u'/11/8b6755210b9011e68400005056c00008', u'type': u'ScaleApplication'}]})
		('action:', u'actions')
		192.168.1.88 - - [26/Apr/2016 17:21:49] "POST /paas/callback HTTP/1.1" 200 -
		('eventType: ', u'deployment_step_success', 'timestamp: ', u'2016-04-26T09:20:26.548Z')
		192.168.1.88 - - [26/Apr/2016 17:21:49] "POST /paas/callback HTTP/1.1" 200 -
		('eventType: ', u'status_update_event', 'timestamp: ', u'2016-04-26T09:20:27.528Z')
		('status', {u'ipAddresses': [], u'timestamp': u'2016-04-26T09:20:27.528Z', u'eventType': u'status_update_event', u'taskStatus': u'TASK_RUNNING', u'host': u'ubuntuServer', u'version': u'2016-04-26T09:20:26.472Z', u'taskId': u'11_8b6755210b9011e68400005056c00008.1cab674b-0b90-11e6-93fa-1e9f5e84c2a3', u'appId': u'/11/8b6755210b9011e68400005056c00008', u'message': u'', u'slaveId': u'bc989b76-a481-4b88-a806-0c0bf770a738-S1', u'ports': [31372]})
		192.168.1.88 - - [26/Apr/2016 17:21:50] "POST /paas/callback HTTP/1.1" 200 -
		('eventType: ', u'deployment_step_success', 'timestamp: ', u'2016-04-26T09:20:27.537Z')
		192.168.1.88 - - [26/Apr/2016 17:21:50] "POST /paas/callback HTTP/1.1" 200 -
		('eventType: ', u'deployment_success', 'timestamp: ', u'2016-04-26T09:20:27.537Z')
		192.168.1.88 - - [26/Apr/2016 17:21:50] "POST /paas/callback HTTP/1.1" 200 -




创建3

		('eventType: ', u'deployment_info', 'timestamp: ', u'2016-04-26T09:25:30.520Z')
		('deployment_id:', u'34a4e419-b35f-4e69-8056-c11eafc0275b')
		('step:', {u'actions': [{u'app': u'/11/4099bf000b9111e6bc3c005056c00008', u'type': u'StartApplication'}]})
		('step:', {u'actions': [{u'app': u'/11/4099bf000b9111e6bc3c005056c00008', u'type': u'ScaleApplication'}]})
		('action:', u'actions')
		192.168.1.88 - - [26/Apr/2016 17:26:53] "POST /paas/callback HTTP/1.1" 200 -
		('eventType: ', u'group_change_success', 'timestamp: ', u'2016-04-26T09:25:30.530Z')
		192.168.1.88 - - [26/Apr/2016 17:26:53] "POST /paas/callback HTTP/1.1" 200 -
		('eventType: ', u'api_post_event', 'timestamp: ', u'2016-04-26T09:25:30.529Z')
		192.168.1.88 - - [26/Apr/2016 17:26:53] "POST /paas/callback HTTP/1.1" 200 -

		('eventType: ', u'deployment_step_success', 'timestamp: ', u'2016-04-26T09:25:30.520Z')
		('deployment_id:', u'34a4e419-b35f-4e69-8056-c11eafc0275b')
		('step:', {u'actions': [{u'app': u'/11/4099bf000b9111e6bc3c005056c00008', u'type': u'StartApplication'}]})
		('step:', {u'actions': [{u'app': u'/11/4099bf000b9111e6bc3c005056c00008', u'type': u'ScaleApplication'}]})
		('action:', u'actions')
		192.168.1.88 - - [26/Apr/2016 17:26:53] "POST /paas/callback HTTP/1.1" 200 -
		('eventType: ', u'deployment_info', 'timestamp: ', u'2016-04-26T09:25:30.519Z')
		('deployment_id:', u'34a4e419-b35f-4e69-8056-c11eafc0275b')
		('step:', {u'actions': [{u'app': u'/11/4099bf000b9111e6bc3c005056c00008', u'type': u'StartApplication'}]})
		('step:', {u'actions': [{u'app': u'/11/4099bf000b9111e6bc3c005056c00008', u'type': u'ScaleApplication'}]})
		('action:', u'actions')
		192.168.1.88 - - [26/Apr/2016 17:26:53] "POST /paas/callback HTTP/1.1" 200 -
		('eventType: ', u'status_update_event', 'timestamp: ', u'2016-04-26T09:25:31.510Z')
		('status', {u'ipAddresses': [], u'timestamp': u'2016-04-26T09:25:31.510Z', u'eventType': u'status_update_event', u'taskStatus': u'TASK_RUNNING', u'host': u'ubuntuServer', u'version': u'2016-04-26T09:25:30.459Z', u'taskId': u'11_4099bf000b9111e6bc3c005056c00008.d1d98b6c-0b90-11e6-93fa-1e9f5e84c2a3', u'appId': u'/11/4099bf000b9111e6bc3c005056c00008', u'message': u'', u'slaveId': u'bc989b76-a481-4b88-a806-0c0bf770a738-S1', u'ports': [31438]})
		192.168.1.88 - - [26/Apr/2016 17:26:54] "POST /paas/callback HTTP/1.1" 200 -
		('eventType: ', u'deployment_step_success', 'timestamp: ', u'2016-04-26T09:25:31.518Z')
		('deployment_id:', u'34a4e419-b35f-4e69-8056-c11eafc0275b')
		('step:', {u'actions': [{u'app': u'/11/4099bf000b9111e6bc3c005056c00008', u'type': u'StartApplication'}]})
		('step:', {u'actions': [{u'app': u'/11/4099bf000b9111e6bc3c005056c00008', u'type': u'ScaleApplication'}]})
		('action:', u'actions')
		192.168.1.88 - - [26/Apr/2016 17:26:54] "POST /paas/callback HTTP/1.1" 200 -
		('eventType: ', u'deployment_success', 'timestamp: ', u'2016-04-26T09:25:31.518Z')
		192.168.1.88 - - [26/Apr/2016 17:26:54] "POST /paas/callback HTTP/1.1" 200 -



删除3
		('eventType: ', u'group_change_success', 'timestamp: ', u'2016-04-26T09:25:58.350Z')
		192.168.1.88 - - [26/Apr/2016 17:27:21] "POST /paas/callback HTTP/1.1" 200 -
		('eventType: ', u'deployment_info', 'timestamp: ', u'2016-04-26T09:25:58.354Z')
		('deployment_id:', u'8c61b7ad-19c3-4953-84b3-edf71a78f189')
		('step:', {u'actions': [{u'app': u'/11/4099bf000b9111e6bc3c005056c00008', u'type': u'StopApplication'}]})
		('action:', u'actions')
		192.168.1.88 - - [26/Apr/2016 17:27:21] "POST /paas/callback HTTP/1.1" 200 -
		('eventType: ', u'status_update_event', 'timestamp: ', u'2016-04-26T09:25:58.983Z')
		('status', {u'ipAddresses': [], u'timestamp': u'2016-04-26T09:25:58.983Z', u'eventType': u'status_update_event', u'taskStatus': u'TASK_KILLED', u'host': u'ubuntuServer', u'version': u'2016-04-26T09:25:30.459Z', u'taskId': u'11_4099bf000b9111e6bc3c005056c00008.d1d98b6c-0b90-11e6-93fa-1e9f5e84c2a3', u'appId': u'/11/4099bf000b9111e6bc3c005056c00008', u'message': u'', u'slaveId': u'bc989b76-a481-4b88-a806-0c0bf770a738-S1', u'ports': [31438]})
		192.168.1.88 - - [26/Apr/2016 17:27:22] "POST /paas/callback HTTP/1.1" 200 -
		('eventType: ', u'app_terminated_event', 'timestamp: ', u'2016-04-26T09:25:58.988Z')
		192.168.1.88 - - [26/Apr/2016 17:27:22] "POST /paas/callback HTTP/1.1" 200 -
		('eventType: ', u'deployment_step_success', 'timestamp: ', u'2016-04-26T09:25:58.988Z')
		('deployment_id:', u'8c61b7ad-19c3-4953-84b3-edf71a78f189')
		('step:', {u'actions': [{u'app': u'/11/4099bf000b9111e6bc3c005056c00008', u'type': u'StopApplication'}]})
		('action:', u'actions')
		192.168.1.88 - - [26/Apr/2016 17:27:22] "POST /paas/callback HTTP/1.1" 200 -
		('eventType: ', u'deployment_success', 'timestamp: ', u'2016-04-26T09:25:58.988Z')
		192.168.1.88 - - [26/Apr/2016 17:27:22] "POST /paas/callback HTTP/1.1" 200 -



创建4

		('eventType: ', u'deployment_info', 'timestamp: ', u'2016-04-26T09:29:33.682Z')
		('deployment_id:', u'7a8701ad-f40c-4581-b1a7-79eda356ea8c')
		('step:', {u'actions': [{u'app': u'/11/d18cd50f0b9111e69040005056c00008', u'type': u'StartApplication'}]})
		('step:', {u'actions': [{u'app': u'/11/d18cd50f0b9111e69040005056c00008', u'type': u'ScaleApplication'}]})
		('action:', {u'app': u'/11/d18cd50f0b9111e69040005056c00008', u'type': u'ScaleApplication'})
		192.168.1.88 - - [26/Apr/2016 17:30:56] "POST /paas/callback HTTP/1.1" 200 -


		('eventType: ', u'deployment_info', 'timestamp: ', u'2016-04-26T09:29:33.681Z')
		('deployment_id:', u'7a8701ad-f40c-4581-b1a7-79eda356ea8c')
		('step:', {u'actions': [{u'app': u'/11/d18cd50f0b9111e69040005056c00008', u'type': u'StartApplication'}]})
		('step:', {u'actions': [{u'app': u'/11/d18cd50f0b9111e69040005056c00008', u'type': u'ScaleApplication'}]})
		('action:', {u'app': u'/11/d18cd50f0b9111e69040005056c00008', u'type': u'StartApplication'})
		192.168.1.88 - - [26/Apr/2016 17:30:56] "POST /paas/callback HTTP/1.1" 200 -

		('eventType: ', u'deployment_step_success', 'timestamp: ', u'2016-04-26T09:29:33.682Z')
		('deployment_id:', u'7a8701ad-f40c-4581-b1a7-79eda356ea8c')
		('step:', {u'actions': [{u'app': u'/11/d18cd50f0b9111e69040005056c00008', u'type': u'StartApplication'}]})
		('step:', {u'actions': [{u'app': u'/11/d18cd50f0b9111e69040005056c00008', u'type': u'ScaleApplication'}]})
		('action:', {u'app': u'/11/d18cd50f0b9111e69040005056c00008', u'type': u'StartApplication'})
		192.168.1.88 - - [26/Apr/2016 17:30:56] "POST /paas/callback HTTP/1.1" 200 -

		('eventType: ', u'group_change_success', 'timestamp: ', u'2016-04-26T09:29:33.696Z')
		192.168.1.88 - - [26/Apr/2016 17:30:56] "POST /paas/callback HTTP/1.1" 200 -
		('eventType: ', u'api_post_event', 'timestamp: ', u'2016-04-26T09:29:33.696Z')
		192.168.1.88 - - [26/Apr/2016 17:30:56] "POST /paas/callback HTTP/1.1" 200 -

		('eventType: ', u'status_update_event', 'timestamp: ', u'2016-04-26T09:29:34.729Z')
		('status', {u'ipAddresses': [], u'timestamp': u'2016-04-26T09:29:34.729Z', u'eventType': u'status_update_event', u'taskStatus': u'TASK_RUNNING', u'host': u'ubuntuServer', u'version': u'2016-04-26T09:29:33.632Z', u'taskId': u'11_d18cd50f0b9111e69040005056c00008.62d3a65e-0b91-11e6-93fa-1e9f5e84c2a3', u'appId': u'/11/d18cd50f0b9111e69040005056c00008', u'message': u'', u'slaveId': u'bc989b76-a481-4b88-a806-0c0bf770a738-S1', u'ports': [31863]})
		192.168.1.88 - - [26/Apr/2016 17:30:57] "POST /paas/callback HTTP/1.1" 200 -
		('eventType: ', u'deployment_success', 'timestamp: ', u'2016-04-26T09:29:34.742Z')
		192.168.1.88 - - [26/Apr/2016 17:30:58] "POST /paas/callback HTTP/1.1" 200 -
		('eventType: ', u'deployment_step_success', 'timestamp: ', u'2016-04-26T09:29:34.742Z')
		('deployment_id:', u'7a8701ad-f40c-4581-b1a7-79eda356ea8c')
		('step:', {u'actions': [{u'app': u'/11/d18cd50f0b9111e69040005056c00008', u'type': u'StartApplication'}]})
		('step:', {u'actions': [{u'app': u'/11/d18cd50f0b9111e69040005056c00008', u'type': u'ScaleApplication'}]})
		('action:', {u'app': u'/11/d18cd50f0b9111e69040005056c00008', u'type': u'ScaleApplication'})
		192.168.1.88 - - [26/Apr/2016 17:30:58] "POST /paas/callback HTTP/1.1" 200 -

删除4


		('eventType: ', u'group_change_success', 'timestamp: ', u'2016-04-26T09:29:58.772Z')
		192.168.1.88 - - [26/Apr/2016 17:31:22] "POST /paas/callback HTTP/1.1" 200 -
		('eventType: ', u'deployment_info', 'timestamp: ', u'2016-04-26T09:29:58.775Z')
		('deployment_id:', u'358a6e8d-753d-4c9a-95bf-7a104ce5baff')
		('step:', {u'actions': [{u'app': u'/11/d18cd50f0b9111e69040005056c00008', u'type': u'StopApplication'}]})
		('action:', {u'app': u'/11/d18cd50f0b9111e69040005056c00008', u'type': u'StopApplication'})
		192.168.1.88 - - [26/Apr/2016 17:31:22] "POST /paas/callback HTTP/1.1" 200 -
		('eventType: ', u'app_terminated_event', 'timestamp: ', u'2016-04-26T09:29:59.313Z')
		192.168.1.88 - - [26/Apr/2016 17:31:22] "POST /paas/callback HTTP/1.1" 200 -
		('eventType: ', u'status_update_event', 'timestamp: ', u'2016-04-26T09:29:59.307Z')
		('status', {u'ipAddresses': [], u'timestamp': u'2016-04-26T09:29:59.307Z', u'eventType': u'status_update_event', u'taskStatus': u'TASK_KILLED', u'host': u'ubuntuServer', u'version': u'2016-04-26T09:29:33.632Z', u'taskId': u'11_d18cd50f0b9111e69040005056c00008.62d3a65e-0b91-11e6-93fa-1e9f5e84c2a3', u'appId': u'/11/d18cd50f0b9111e69040005056c00008', u'message': u'', u'slaveId': u'bc989b76-a481-4b88-a806-0c0bf770a738-S1', u'ports': [31863]})
		192.168.1.88 - - [26/Apr/2016 17:31:22] "POST /paas/callback HTTP/1.1" 200 -
		('eventType: ', u'deployment_success', 'timestamp: ', u'2016-04-26T09:29:59.313Z')
		192.168.1.88 - - [26/Apr/2016 17:31:22] "POST /paas/callback HTTP/1.1" 200 -
		('eventType: ', u'deployment_step_success', 'timestamp: ', u'2016-04-26T09:29:59.313Z')
		('deployment_id:', u'358a6e8d-753d-4c9a-95bf-7a104ce5baff')
		('step:', {u'actions': [{u'app': u'/11/d18cd50f0b9111e69040005056c00008', u'type': u'StopApplication'}]})
		('action:', {u'app': u'/11/d18cd50f0b9111e69040005056c00008', u'type': u'StopApplication'})
		192.168.1.88 - - [26/Apr/2016 17:31:22] "POST /paas/callback HTTP/1.1" 200 -

