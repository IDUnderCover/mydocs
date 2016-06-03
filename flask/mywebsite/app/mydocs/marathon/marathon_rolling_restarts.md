## Application Deployments


在marathon中，所有应用和应用组的操作都以deployment为运行单位，一个development可以包含多个动作，例如  

- 启动/停止 一个或多个应用
- 升级一个或多个应用
- 扩展一个或多个应用

多个deployments 可以同时进行，前提是他们之间的不会操作同一个 application。


如果 Applications 之间没有依赖，那么他们可以以任意的顺序启动。 如果application之间存在依赖关系，那么deployment会按特定的顺序来启动application

![dependencies](http://i.imgur.com/APhLWno.png)



在上图中，一个application group 由 两个 application 组成，分别为 /product/database 和 /product/service，而且 sercice 依赖于 database。


1. 启动时，db先将被启动，然后是app
2. 停止时，app先被停止，然后是db
3. 升级时，marathon 采用 rolling restart 方法，先启动新版本的applications，将服务过渡到新系统后，再停止旧版本系统。
4. 扩展时，db 将优先于 app 扩展


###Rolling Restarts

在服务升级过程中，为了使得原先的服务不会受到升级过程影响，旧版本的applications必须维持在一定数量，来保持服务的稳定性。 marathon 中利用 minimumHealthCapacity 来定义升级过程中旧版本应用的最少运行数。

- minimumHealthCapacity == 0 ： 在启动新实例前，所有的旧实例将会被停止。
- minimumHealthCapacity == 1 ： 在启动新实例前，旧实例不受影响。
- minimumHealthCapacity 在 0 1 之间： 先将旧实例缩减到所允许的最低数（instance * minimumHealthCapacity），然后再启动相同数目的新实例。如果过程顺利，那么最终新实例将会被扩展到100%

已上图中的应用组升级为例，升级步骤如下：   
1. 将旧db实例缩减到6个 （10 * 0.6）  
2. 启动6个新db实例  
3. 将旧app实例缩减到16 （20 * 0.8）  
4. 启动16个新app实例  
5. 停止所有旧app实例  
6. 停止所有旧db实例   
7. 将新db实例扩展到10个    
8. 将新app实例扩展到20个  







reference:  
https://mesosphere.github.io/marathon/docs/deployments.html