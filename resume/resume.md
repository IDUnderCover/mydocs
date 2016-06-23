##个人简历

基本信息    

* 姓名： 倪佳良    
* 电话：18251901697
* 邮箱：njl@modelinking.com
* 学历：本科
* 工作年限： 1年
* 求职意向：Python， Docker 开发
---
###教育经历 

<table>
    <tr>
        <td>时间</td>
	<td>学校</td>
	<td>专业</td>
    </tr>
    <tr>
        <td>2011.09-2015.07</td>
	<td>南京工业大学</td>
	<td>信息计算科学</td>
    </tr>
</table>

GPA(3.6)  在校获得多次校奖学金, 校外奖学金。

###实验室项目
***TWR03D型天气雷达终端操控软件及其二次产品开发  &#160;&#160;&#160;&#160;  2013/09 - 2013/12***

简介: 该项目为多普勒雷达软件项目, 分为雷达控制端和二次产品软件. 控制端负责对雷达的扫描控制, 实时接收雷达数据并动态显示;二次产品利用采集的数据为基础, 利用各个产品的算法生成二次产品.

相关技术：`C++, MFC`

在项目后期开发时加入, 团队为五个研究生和我, 他们负责雷达数据处理算法的实现和控制端, 我的工作主要为
	
* 用 `MFC C++ socket` 实现雷达数据传输控制
* 阅读相关的文献资料，实现雨强显示，累积降雨和二维风场反演算法


----

###工作经历   


| 时间 | 公司 | 职位 |规模|
| -----|:----:| ----:|----:|
| 2015.07-2016.05 | 南京振古信息科技有限公司     | 研发工程师   |少于15人|

主要职责：PaaS平台开发，Python后端开发，Docker相关技术的研究。

---
###工作项目经验

***数据邦 &#160;&#160;&#160;&#160;   2015/09-2016/05***

简介: 数据邦是一个数据在线分析平台，用户可上传其所需要分析的数据，通过 `web` 桌面在线编写脚本完成分析。相应的数据和脚本也可用来分享或交易。
相关技术：`Python, Flask, Docker, Mesos `
从最初就参与了整个平台的设计和开发，学习了许许多多Docker 生态圈内的技术，主要工作内容如下

1. 基于`docker vloume` 插件 [`convoy`](https://github.com/rancher/convoy), `NFS` 为后端存储，实现数据跨主机共享.
2. 基于 `zookeeper` 搭建 `overlay` 网络，为每个容器分配唯一 `IP`，`mesos-dns` 作为服务发现.
3. 利用 `Python Flask` 对 [marathon](https://mesosphere.github.io/marathon/) 提供的 `API` 进行封装, 开发容器操作的RESTFul API 供其他开发人员调用.
4. 数据分析工具的docker image 制作, 比如 [qgis](http://www.qgis.org/en/site/), [grassgis](http://grass.osgeo.org/), Jupyter等，以及私有镜像仓库的部署.
5. 基于 `Hadoop NFS Gateway` 实现在容器中挂载大数据文件.
6. [guacamole](http://guacamole.incubator.apache.org/) web 桌面代理的开发部署, 以及 `nginx `配置管理

**朗诗地产数据中心  &#160;&#160;&#160;&#160; 2015/07-2015/11**
简介： 朗诗绿色地产内部内容管理平台，用于文档管理，影像内容捕获，工作流和邮件管理等。将第三方系统，如ERP，400电话系统，招投标等系统的数据全部存储在Filenet P8中。
相关技术：`Java, Jersey, Oracle`,  [IBM Filenet P8](https://www.ibm.com/support/knowledgecenter/SSNW2F_5.2.1/com.ibm.p8toc.doc/welcome_p8.htm)
个人职责:

1. 用`Jersey` 开发`Filenet`的 `API` 提供给第三方调用
2. 第三方系统文档数据属性的建模
3. 现场协调安装部署`Filenet`部分组件


---
###个人技能：

* 良好的英文阅读能力，英语6级， 雅思 6.5
* 熟悉  `python`， `Flask`，
* 熟悉`Scrapy`爬虫框架，抓取过优酷视频信息，拉勾职位信息。
* 熟悉 `Java`， `C++`， `MATLAB`, `SQL`
* 熟练使用 `docker`，了解`CGroup`, `namespace`，`runc`，`containerd`
* 熟悉 `marathon`, `mesos` 
* 熟悉 `linux` 常用命令，`systemd`服务管理，`git` 
* 熟悉 nginx 配置

###自我评价
	
热爱学习互联网技术，在 `Coursera edx` 上完成多门课程。 在创业公司的一年里，磨练了意志，抗压能力强。自我驱动。

完成的课程列表

1. [Stanford University: Machine Learning](https://www.coursera.org/learn/machine-learning)   [课程证书](http://o913sn63o.bkt.clouddn.com/Coursera-ml.pdf)
2. [Johns Hopkins University: R  Programming ](https://www.coursera.org/learn/r-programming)[课程证书](http://o913sn63o.bkt.clouddn.com/Coursera-rprog.pdf)
3. [BerkeleyX: CS100.1x Introduction to Big Data with Apache Spark](https://courses.edx.org/courses/BerkeleyX/CS100.1x/1T2015/info) [课程证书](https://s3.amazonaws.com/verify.edx.org/downloads/45919685f8df47f08e590679b954b30f/Certificate.pdf)
4. [BerkeleyX: CS190.1x Scalable Machine Learning](https://courses.edx.org/courses/BerkeleyX/CS190.1x/1T2015/info)  [课程证书](https://s3.amazonaws.com/verify.edx.org/downloads/40754021da08441197bb3e9b96e91826/Certificate.pdf)




