---
layout: post
title: Gouge Away
description: Incorporating SQOOP in your Data Pipeline
image: /assets/img/SQOOP-post/scoop.jpg
noindex: true
---

# Gouge Away

You have just [completed](../2019-02-01-EMR-post) setting up your new and shiny _EMR_ cluster, and want to unleash the full power of _Spark_ on the nearest data-source.

All you need to do, is pass the location of the data in your _S3 Bucket_ and employ the parallel capabilities of _HDFS_.

However, all your data is stored on a _MySQL_ database.

One thing you can do is read the data with _Spark_ and a _JDBC_ connector from the database to a _Spark Dataframe_:

<script src="https://gist.github.com/wolfenfeld/44bbc180a022dac7aa1cd85a6e56217d.js">
</script>

This is nice, but there is a better way.

This post comes after trying several approaches to get the easiest, cleanest, scalable and best performing data ingestion solution for the case of data stored on a _MySQL_ server.

The goal of this post is to provide an easy and comprehensive, step by step, guide, on how to use _Sqoop_ and incorporate it to your _EMR_ job flow.

You can find a a walk-through on how to setup and launch an _EMR_ cluster [here](../2019-02-01-EMR-post).

In this post we will start with a brief introduction to _Sqoop_, continue with formulating the problem, go over the necessary tools and finally describe the proposed solution.

Small disclaimer - an active _AWS_ account is necessary for this tutorial.

# What is Scoop

_Apache Sqoop_ (_SQL_ to _Hadoop_) is a tool designed for efficient transfer of data between _Apache Hadoop_ and structured data-stores (in our case - relational databases).

We will only scratch the surface on architecture of _Sqoop_, and briefly explain the import processes in high level.

_Sqoop_ automates most of data transfer, relying on the database to describe the schema for the data to be imported. _Sqoop_ uses _MapReduce_ to import and export the data, which provides parallel operation as well as fault tolerance.

<figure>
  <img alt="An image with a caption" src="/assets/img/SQOOP-post/sqoop-arch.png" class="lead" data-width="432" data-height="414">
  <figcaption>Image Credits devx.com.</figcaption>
</figure>

The import procedure (as described in the diagram above) goes through the following steps:

1. _Scoop_ (client) pulls the metadata from the database.
2. Launches several _MapReduce_ jobs.
3. Each _MapReduce_ job pulls its share of data from the database.
4. Each _MapReduce_ job writes the data to its target location.

Later we will show how to configure the number of _MapReduce_ jobs to best fit the number of connections to the database.

# Problem Formulation

The problem that we are facing can be broken down into 3 (as always) sub-problems:

- Spinning up a cluster with all the relevant dependencies.
- Connecting to a _MySQL_ server and fetching the data with _Sqoop_.
- Storing the data.

# Tools Description

In our solution we will use the following tools:

- _Apache Spark_ - an open-source distributed general-purpose cluster-computing framework.
- _Sqoop_ - a tool designed to transfer data between _Hadoop_ and relational databases.
- _Pyspark_ - the Python API for _Spark_.
- _EMR_ service - _Elastic Map Reduce_ is _AWS_ managed _Hadoop_ framework.
- _S3_ service - _AWS_ storage service.
- Boto 3 - Boto is the AWS SDK for Python. It enables Python developers to create, configure, and manage _AWS_ services.

# Solution Formulation

In my [previous post](../2019-02-01-EMR-post) we have seen how to spin up an _EMR_ cluster, pull the data from a _MySQL_ server (using _Spark_) and load it to _S3_.

We will use the same code, and only swap the _"extract_data_from_db"_ method with _"extract_data_from_db_with_sqoop"_.

Another thing you will need to do is add {'Name': 'Sqoop'} to the applications list (in the **load_cluster** method in the **EMRHandler** class)

```
Applications=[{'Name': 'Spark'}, {'Name': 'JupyterHub'}, {'Name': 'Hive'},{'Name': 'Sqoop'}]
```

Our solution ([as in the previous post](../2019-02-01-EMR-post)) is broken down to 3 main scripts and a configuration file.

- EMR Handler - the python script that is in charge of spinning-up, configuring and running the _EMR_ cluster.
- Bootstrap - this script is used to configure each node in the cluster.
- Processing - the python script that executes the data processing commands.

As stated, the solution is identical to the one described in the [previous post](../2019-02-01-EMR-post) apart from extracting method.

In the **extract_data_from_db_with_sqoop** method we are using the _os.system(sqoop_command)_ command to execute the _Sqoop import_ command.

It is comprised of the following parameters:

- driver - the _MySQL_ driver
- connect - the database url
- username and password - the credentials for connecting to the database
- query - the query of the extracted data
- num-mappers - the number of mappers (for each node) that will fetch the data
- split-by - the column on which the mappers divide among themselves the workload
- target-dir - the destination of the transfered data
- --as-parquetfile - a flag indicating the format of the extracted data (parquet file in our case)

<script src="https://gist.github.com/wolfenfeld/ecbaa81c8f971d7cf667ad26d77fe40a.js">
</script>

Several important points:

1. As you can see, we are saving the data and then reading with _Spark_ the parquet file and returning the Dataframe.
2. I have made several attempts to extract the data to a _S3_ bucket without success (EMR release 5.22.0) - this should probably be fixed in later releases.
3. The bigger the number of mappers you allocate - the faster the extraction be completed. However, you should not exceed the number of database connections.

# Conclusion

In this tutorial we have gone through the steps needed to spin-up an _EMR_ Cluster, read the relevant data from a _MySQL_ database, and finally load the results to _S3_.

I hope this guide helped shed some light on how to use _EMR_ and _Sqoop_ to achieve the relevant results.
