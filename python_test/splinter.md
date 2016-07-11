##Splinter


####简介
splinter是自动测试web应用的工具，可以模拟浏览器操作。  

首先需要下载chrome 驱动
https://sites.google.com/a/chromium.org/chromedriver/downloads


	from splinter import Browser
	b = Browser('chrome')
	b.visit('https://www.baidu.com')

	#  Fill the field identified by ``name`` with the content specified by ``value``
	b.fill ('wd','splinter')



	在chrome console 中使用 xpath 来提取相应元素
	获取邮箱地址的input
	$x("//input[@placeholder='请输入常用邮箱地址']")
	# 因为有两种注册方式，一种基于手机，另一种基于邮箱方式，在这里选择了第二种
	$x("//input[@placeholder='请输入密码']")[1]
	# 找工作按钮
	$x("//input[@value='找工作']")[1]
	# 阅读协议按钮
	$x("//span[@class='checkbox_icon']")[1]
	# 注册提交按钮
	$x("//input[@class='btn btn_green btn_active btn_block btn_lg']")[1]
