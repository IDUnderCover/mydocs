## Week 2

join( other, on, how)
other: right side of the join
on: join column name, list of column (names), or join expression
how: inner, outer, left_outer, right_outer, left_smi

X.join(Y, cols)

inner join:  return DF of rows with matching cols in both X and Y
outer : return DF of rows with matching cols in either X and Y
left_outer: return DF of rows with matching cols in  X
right_outer: return DF of rows with matching cols in  Y

default: inner join 


####cs105_lab1a_spark_tutorial  
1. The driver has Spark jobs that it needs to run and these jobs are split into tasks that are submitted to the executors for completion. The results from these tasks are delivered back to the driver.

2. normal python code gets executed in the Spark driver's JVM

3. start a new Spark application by creating a SparkContext. Then you can create a SQLContext from the SparkContext.

4.  在Spark文档中, 这些Threads经常被引用为cores, 其实他与物理机的CPU Cores 一点关系都没有.
5. DataFrame is immutable, so once created, it cannot be changed. As a result, each transformation creates a new DataFrame.

6. Lazy Evaluation, no transformation are executed until an action occurs.

7.  python package fake-factory  

8.  dataDF.printSchema() 查看DataFrame的schema, dataDF.rdd.getNumPartitions() 查看该dataFrame会被分成几个partitions

9. [Deep Dive into Spark SQL’s Catalyst Optimizer](https://databricks.com/blog/2015/04/13/deep-dive-into-spark-sqls-catalyst-optimizer.html)

10. 在databricks 中 可用 display(dataDF) 来查看df, 显示效果更好

11. fist() and take() actions depend on  how the DataFrame is partitioned

12. sample() 随机抽样

13. cache() 

		# Cache the DataFrame
		filteredDF.cache()
		# Trigger an action
		print filteredDF.count()
		# Check if it is cached
		print filteredDF.is_cached

	unpersist()
		# If we are done with the DataFrame we can unpersist it so that its memory can be reclaimed
		filteredDF.unpersist()
		# Check if it is cached
		print filteredDF.is_cached


14. Spark executes using a Java Virtual Machine (JVM). pySpark runs Python code in a JVM using Py4J

![](http://o913sn63o.bkt.clouddn.com//edx/spark/diagram-2a.png)  
![](http://o913sn63o.bkt.clouddn.com//diagram-2a.png)
![](http://o913sn63o.bkt.clouddn.com/diagram-3d.png)
![](http://o913sn63o.bkt.clouddn.com/diagram-3e.png)
![](http://o913sn63o.bkt.clouddn.com/diagram-3f.png)
