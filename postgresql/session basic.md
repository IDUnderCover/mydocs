##SQLAlchemy Session Basics


Session 建立了与 数据链接的会话通道, 并开辟了一块区域用来保存你所涉及到的所有对象(在其生命周期里).  Session 可以创建一个 query 对象, 用来进行一些基本的插入查询等操作. 重要的是, session 里有一个特殊的数据结构 Identity Map, 维护了对象与主键之间的映射关系. 数据表里主键是唯一的, 每个主键对应的行也是唯一的, 当某数据行被转换成了python 对象 A, 他们两就绑定起来了, 所有对该对象 A 的操作会成为对该行的操作, 即使从数据库中查询出该行并复制给一个新的对象B, A 和 B 代表着同一对象 id(A) == id(B)

![Identity Map](http://martinfowler.com/eaaCatalog/idMapperSketch.gif) 

####Getting a Session

	from sqlalchemy import create_engine
	from sqlalchemy.orm import sessionmaker
	
	# an Engine, which the Session will use for connection
	# resources
	some_engine = create_engine('postgresql://scott:tiger@localhost/')
	
	# create a configured "Session" class
	Session = sessionmaker(bind=some_engine)
	
	# create a Session
	session = Session()
	
	# work with sess
	myobject = MyObject('foo', 'bar')
	session.add(myobject)
	session.commit()

sessionmaker 创建了一个预配置好的 sesssion工厂类, 之后所有用Session()来创建的ses都会使用此engine作为链接, 当然我们也可以在 创建ses的时候 重新绑定新的参数.


一般情况下, 都将 sessionmaker 写在包内的__init__.py下, 这样通过 from package import Session , 可以共用同一个配置好的Session

#### Transaction scope
当一个session开始与数据库交换数据时, 就表明一个事务开始了,直到被 rollback commit或者close就结束事务, Session 随后也可以开启一个新的事务,不过一次只能处理一个事务. 



####Is the Session a cache?

Yeee...no. It’s somewhat used as a cache, in that it implements the identity map pattern, and stores objects keyed to their primary key. However, it doesn’t do any kind of query caching. This means, if you say session.query(Foo).filter_by(name='bar'), even if Foo(name='bar') is right there, in the identity map, the session has no idea about that. It has to issue SQL to the database, get the rows back, and then when it sees the primary key in the row, then it can look in the local identity map and see that the object is already there. It’s only when you say query.get({some primary key}) that the Session doesn’t have to issue a query.

Additionally, the Session stores object instances using a weak reference by default. This also defeats the purpose of using the Session as a cache.

The Session is not designed to be a global object from which everyone consults as a “registry” of objects. That’s more the job of a second level cache. SQLAlchemy provides a pattern for implementing second level caching using dogpile.cache, via the Dogpile Caching example.

####Session的基础使用方法




reference:
http://docs.sqlalchemy.org/en/latest/orm/session_basics.html#session-faq-whentocreate
	

