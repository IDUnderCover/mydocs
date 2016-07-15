## week 1 

###The Structure Spectrum

Unstructured (schema-nerver): Plain Text, Media 

perform ETL (Extract-Transform-Load)  on unstructured data =>

Semi-Structured(schema-later): Documents XML, Tagged Text/Media, Tabular data

Structured(schema-first) : Relational Database, Formatted Messages

####A Spark program is two programs

1. Driver program run on local
2. Worker programs run on cluster nodes or in local threads

####Spark and SQL Contexts

A Spark program first creates a SparkContext object, which tells Spark how and where to access a cluster.

Example: Creating SparkContext in Jupyter
![](/home/razaura/下载/ebe94c6e-9c95-476d-82de-9e29ce815426.png) 


####DataFrames
1. Immutable once constructed
2. Track lineage information to efficiently recompute lost data
3. Enable operations on collection of elements in parallel

How to construct DataFrames?

1. by parallelizing existing Python collections
2. by transforming an existing Spark or pandas DFs
3. from files in HDFS or any other storage system

Each row of DataFrame is a Row object

Operations

transformations 
1. lazy evaluation(not computed immediately)
2. executed when action runs on it

Using Catalyst to optimize the required calculations

User Defined Function Transformations (udf)
slen = udf(lambda s: len(s), IntegerType())

persist or cache data frames in memory or on disk, avoid recomputing  

actions:




Reference:

[Spark SQL, DataFrames and Datasets Guide](https://spark.apache.org/docs/latest/sql-programming-guide.html)
