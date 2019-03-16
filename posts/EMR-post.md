# Taming the Hydra

## Outline

1. Intro
2. Problem formulation
3. Tools description
4. Solution formulation
5. Conclusion

## Intro

Whenever you need to slice and dice a massive dataset, and _pandas_ or _SQL_ cannot do the trick - pam pam pam, Spark is here have no fear.

This post comes after long and lonesome search for a tutorial on how to spin-up an EMR Cluster, read the relevant data from a table in RDS, executes a set of commands using Pyspark and dump the results to S3.

The goal of this post is to provide an easy and comprehensive, step by step, guide, and save the time and frustration to anyone who wishes to construct such a system.

Small disclaimer - an active AWS account is necessary for this tutorial.

## Problem Formulation

The problem that we are facing can be broken down into 3 (as always) sub-problems:

- Spinning up a cluster with all the relevant dependencies.
- Connecting to a data source for fetching and dumping the data.
- Processing the raw data using the _Spark_ framework.

## Tools description

In our solution we will use the following tools:

- Apache Spark - an open-source distributed general-purpose cluster-computing framework.
- Pyspark - the Python API for Spark.
- EMR service - Elastic Map Reduce is AWS managed Hadoop framework.
- S3 service - AWS storage service.
- Boto 3 - Boto is the AWS SDK for Python. It enables Python developers to create, configure, and manage AWS services.

## Solution formulation

Our solution is comprised of 3 main scripts.

- EMR loader - the python script that is in charge of spinning-up, configuring and running the EMR cluster.
- Bootstrap - this script is used to configure each node in the cluster.
- Processing - the python script that executes the data processing commands.

## Conclusion

In this tutorial we have gone through the steps needed to spin-up an EMR Cluster, read the relevant data from a table in RDS, executes a set of commands using Pyspark and dump the results to S3.

I hope this guide helped shed some light on how to use EMR to achieve the relevant results and would like to thank @nimrod_milo for helping me on this glorious quest.
