##SQLAlchemy 

####quickstart
	
	In [1]: import sqlalchemy
	
	In [2]: sqlalchemy.__version__
	Out[2]: '1.0.12'
	
	In [3]: from sqlalchemy import create_engine
	
	# 使用sqlite3内存数据库, echo 设置了所有 sql 生成输出
	In [4]: engine = create_engine('sqlite:///:memory:', echo=True)
	
####建立映射关系

	In [5]: from sqlalchemy.ext.declarative import declarative_base

	# 该类维护了表和类之间如何进行映射，我们的类都将派生于该类
	In [6]: Base = declarative_base()

	# 定义 User 类
	class User(Base):
	    __tablename__ = 'users'
	
	    id = Column(Integer, primary_key=True)
	    name = Column(String)
	    fullname = Column(String)
	    password = Column(String)
	
	    def __repr__(self):
	       return "<User(name='%s', fullname='%s', password='%s')>" % (
	                            self.name, self.fullname, self.password)
		

>When our class is constructed, Declarative replaces all the Column objects with special Python accessors known as descriptors; this is a process known as instrumentation. The “instrumented” mapped class will provide us with the means to refer to our table in a SQL context as well as to persist and load the values of columns from the database.


在User类创建完成后，通过 __table__ 属性，可以看到表的元数据

	>>> User.__table__ 
	Table('users', MetaData(bind=None),
	            Column('id', Integer(), table=<users>, primary_key=True, nullable=False),
	            Column('name', String(), table=<users>),
	            Column('fullname', String(), table=<users>),
	            Column('password', String(), table=<users>), schema=None)



什么是MetaData？
>A collection of Table objects and their associated schema constructs.
>
>Holds a collection of Table objects as well as an optional binding to an Engine or Connection. If bound, the Table objects in the collection and their columns may participate in implicit SQL execution.
>
>The Table objects themselves are stored in the MetaData.tables dictionary.
>
>MetaData is a thread-safe object for read operations. Construction of new tables within a single MetaData object, either explicitly or via reflection, may not be completely thread-safe.

MetaData就是一个registry，他能将我们定义的类转换成一系列的sql 命令交给database来执行。通过调用MetaData.create_all() 方法，engine作为与数据库链接源。
	
	In [11]: Base.metadata.create_all(engine)
	2016-07-08 16:21:52,106 INFO sqlalchemy.engine.base.Engine SELECT CAST('test plain returns' AS VARCHAR(60)) AS anon_1
	2016-07-08 16:21:52,106 INFO sqlalchemy.engine.base.Engine ()
	2016-07-08 16:21:52,107 INFO sqlalchemy.engine.base.Engine SELECT CAST('test unicode returns' AS VARCHAR(60)) AS anon_1
	2016-07-08 16:21:52,107 INFO sqlalchemy.engine.base.Engine ()
	2016-07-08 16:21:52,109 INFO sqlalchemy.engine.base.Engine PRAGMA table_info("users")
	2016-07-08 16:21:52,109 INFO sqlalchemy.engine.base.Engine ()
	2016-07-08 16:21:52,110 INFO sqlalchemy.engine.base.Engine 
	CREATE TABLE users (
		id INTEGER NOT NULL, 
		name VARCHAR, 
		fullname VARCHAR, 
		password VARCHAR, 
		PRIMARY KEY (id)
	)
	
	
	2016-07-08 16:21:52,111 INFO sqlalchemy.engine.base.Engine ()
	2016-07-08 16:21:52,111 INFO sqlalchemy.engine.base.Engine COMMIT
	
#### 创建一个映射实例

	In [13]: ed_user = User(name = 'ed', fullname='Ed Jones', password='edspassword')
	
	In [14]: ed_user.name
	Out[14]: 'ed'
	
	In [15]: ed_user.password
	Out[15]: 'edspassword'
	
	In [16]: str(ed_user.id)
	Out[16]: 'None'

####创建一个会话[Session](http://docs.sqlalchemy.org/en/latest/orm/session_api.html#sqlalchemy.orm.session.Session)


	# sessionmaker  A configurable Session factory.
	In [18]: from sqlalchemy.orm import sessionmaker
	# 配置好session工厂
	In [19]: Session = sessionmaker(bind=engine)
	# 创建一个session
	In [21]: session = Session()

>The above Session is associated with our SQLite-enabled Engine, but it hasn't opened any connections yet. When it's first used, it retrieves a connection from a pool of connections maintained by the Engine, and holds onto it until we commit all changes and/or close the session object.

####增加更新对象

	# add 方法调用后， ed_user并没有直接写入到数据库，而是pending状态, 直到 flush被调用
	In [23]: session.add(ed_user)
	
	# 调用flush 将数据写入
	In [24]: session.flush()
	2016-07-08 17:07:54,724 INFO sqlalchemy.engine.base.Engine BEGIN (implicit)
	2016-07-08 17:07:54,727 INFO sqlalchemy.engine.base.Engine INSERT INTO users (name, fullname, password) VALUES (?, ?, ?)
	2016-07-08 17:07:54,727 INFO sqlalchemy.engine.base.Engine ('ed', 'Ed Jones', 'edspassword')

	# 查询刚才所提交的数据
	our_user = session.query(User).filter_by(name='ed').first()
	
	# 发现返回的对象相同
	>>> ed_user is our_user
	True

为什么会返回同一对象？

>The ORM concept at work here is known as an identity map and ensures that all operations upon a particular row within a Session operate upon the same set of data. Once an object with a particular primary key is present in the Session, all SQL queries on that Session will always return the same Python object for that particular primary key; it also will raise an error if an attempt is made to place a second, already-persisted object with the same primary key within the session.

`identity map` 保证了在一个会话中， 所有queries 会为特定的主键返回同一对象。在上述测试例子中，ed_user 主键 为 1, 所查询到的数据行主键也为 1 ， 所以返回的就是ed_user

一次也可将多个对象加入session

	>>> session.add_all([
	...     User(name='wendy', fullname='Wendy Williams', password='foobar'),
	...     User(name='mary', fullname='Mary Contrary', password='xxg527'),
	...     User(name='fred', fullname='Fred Flinstone', password='blah')])

在加入后，session将跟踪这些值的变化情况

	session.dirty 哪些对象发生了变化
	session.new  新增了哪些新的对象

最后通过 session.commit() 将所有变化记录提交

>commit() flushes whatever remaining changes remain to the database, and commits the transaction. The connection resources referenced by the session are now returned to the connection pool. Subsequent operations with this session will occur in a new transaction, which will again re-acquire connection resources when first needed.



	
	
reference：
	http://docs.sqlalchemy.org/en/latest/orm/tutorial.html