---
layout: post
title: Gouge Away
description: Incorporating SQOOP in your Data Pipeline
image: /assets/img/SQOOP-post/scoop.jpg
noindex: true
---

# Gouge Away

You have just completed setting up your new and shiny EMR cluster, and want to unleash the full power of _Spark_ on the nearest data-source.

All you need to do, is pass the location of the data in your _S3 Bucket_ and employ the parallel capabilities of HDFS.

However, all your data is stored on a MySQL database.

You can read the data with _Spark_ and a JDBC connector from the database to a _Spark Dataframe_:

<script src="https://gist.github.com/wolfenfeld/44bbc180a022dac7aa1cd85a6e56217d.js">
</script>

This is nice, but there is a better way.

This post comes after trying several approaches to get the easiest, cleanest, scalable and best performing data ingestion solution for the case of data stored on a MySQL server.

The goal of this post is to provide an easy and comprehensive, step by step, guide, on how to use SQOOP and incorporate it to your EMR job flow.

You can find a a walk-through on how to setup and launch and _EMR cluster_ here.

In this post we will start with formulating the problem, go over the necessary tools and finally describe the proposed solution.

Small disclaimer - an active AWS account is necessary for this tutorial.

# What is Scoop

Apache Sqoop (SQL to Hadoop) is a tool designed for efficient transfer of data between Apache Hadoop and structured data-stores (in our case - relational databases).

I will not get into too much details on architecture of SQOOP, and only explain the import processes in high level.

Sqoop automates most of data transfer, relying on the database to describe the schema for the data to be imported. Sqoop uses MapReduce to import and export the data, which provides parallel operation as well as fault tolerance.

![Full-width image](https://wolfenfeld.github.io/jewpyter/assets/img/SQOOP-post/sqoop-arch.png){:.lead data-width="432" data-height="414"} Image Credits devx.com. {:.figure}

# Problem Formulation

The problem that we are facing can be broken down into 3 (as always) sub-problems:

- Spinning up a cluster with all the relevant dependencies.
- Connecting to a MySQL server and fetching the data with SQOOP.
- Storing the data in S3.

# Tools Description

In our solution we will use the following tools:

- Apache Spark - an open-source distributed general-purpose cluster-computing framework.
- SQOOP - a tool designed to transfer data between Hadoop and relational databases.
- Pyspark - the Python API for Spark.
- EMR service - Elastic Map Reduce is AWS managed Hadoop framework.
- S3 service - AWS storage service.
- Boto 3 - Boto is the AWS SDK for Python. It enables Python developers to create, configure, and manage AWS services.

# Solution Formulation

And now for the good stuff.

Our solution is broken down to 3 main scripts and a configuration file.

- EMR Handler - the python script that is in charge of spinning-up, configuring and running the EMR cluster.
- Bootstrap - this script is used to configure each node in the cluster.
- Processing - the python script that executes the data processing commands.

We will start with the EMR Handler - in the following gist we see the initialization of the EMR Handler object with the values form the configuration file. Also, we find the _load cluster_ method - which calls the the EMR service using the _boto client_.

<script src="https://gist.github.com/wolfenfeld/7920ff08c4e1e0d4274f752be1a40050.js">
</script>

Lets drill down on each of the arguments of the _load cluster_ method, for they are the essential part of configuring the cluster to suite our task.

- Name - the name of the cluster.
- LogUri - where the generated logs are stored.
- ReleaseLabel - the software version (5.20 at the time when this post was written)
- Instances - the instance, of which the cluster is composed of, configuration .
- Applications - application necessary for running the tasks at hand.
- BootstrapActions - the configuration of the actions that each node (instance) will take prior to processing phase, in our case setting all the dependencies.
- JobFlowRole, ServiceRole - Roles for security.
- Configurations - spark environment configurations.
- Tags - for reporting or filtering.
- Steps - the steps that are submitted.

For the sake of readability, a method is defined for each major argument:,

**Instance Configuration**

Here, I believe, the parameters are very self explanatory, apart from InstanceCount, that receives an integer _N_ that defines _N-1_ slaves and a single master:

<script src="https://gist.github.com/wolfenfeld/e86dcd95f13346a4efd01478ee762a48.js">
</script>

**Bootstrap Actions Configuration**

Defines where the Bootstrap script is located on S3:

<script src="https://gist.github.com/wolfenfeld/09c152c3faa8c7151dd304be18cc1538.js">
</script>

**Spark Configuration**

Defines the environment variables necessary to use _Pyspark_ in the submitted tasks (we are going to use the _Conda's_ python interpreter as our _Pyspark_ interpreter):

<script src="https://gist.github.com/wolfenfeld/99302e69de33e49901990c7a48c6033f.js">
</script>

An important part here is the _extra-paths_ section that is needed for the use of the MySQL connector.

**Tag Configuration**

<script src="https://gist.github.com/wolfenfeld/41a42255bd145f23183cbd46331cfc77.js">
</script>

**Steps Configuration**

Defines the steps that will run one spark-submit will be initiated:

<script src="https://gist.github.com/wolfenfeld/03814c02499f44b48b722379ab3900fd.js">
</script>

An important part in the 'Run Computations Script' step is the '--packages' parameters that are needed for the MySQL connector.

**Auxiliary Functions**

For uploading the files to S3:

<script src="https://gist.github.com/wolfenfeld/72649e2bb2f882d73edbb631f58f095d.js">
</script>

**Run Function**

Constructing the EMR handler, uploading the necessary files to S3, and loading the cluster:

<script src="https://gist.github.com/wolfenfeld/271e6d96e2e6e696147c7562adae3c20.js">
</script>

**EMR Service Configuration File**

A yml file containing all the necessary parameters:

<script src="https://gist.github.com/wolfenfeld/a9459158a98f191c338e7aaa17c4e26e.js">
</script>

**Bootstrap Actions Script**

Installing _Conda_ and all the necessary dependencies.

<script src="https://gist.github.com/wolfenfeld/1a41bc595d21ed1f71421344d27e1360.js">
</script>

**Process Data Script**

The file that is uploaded to S3 and executed in one of the spark-submit steps.

It contains a method for extracting data from RDS using _Spark_, processing this data, and loading the results to S3,

The processing itself is only a select column operation, and can be substituted by any _Spark_ functionality that you wish.

This file also shows the proper way to use a logger within the EMR cluster.

<script src="https://gist.github.com/wolfenfeld/05c26adec1f6b5185da08e9317ffc74e.js">
</script>

# Conclusion

In this tutorial we have gone through the steps needed to spin-up an EMR Cluster, read the relevant data from a table in RDS, executes a set of commands using Pyspark and finally load the results to S3.

I hope this guide helped shed some light on how to use EMR to achieve the relevant results and would like to thank @nimrod_milo for helping me on this glorious quest.
