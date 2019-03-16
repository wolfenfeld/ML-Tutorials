# Taming the Hydra

## Outline

1. Intro
2. Problem formulation
3. Tools description
4. Solution formulation
5. Conclusion

## Intro

Whenever you need to slice and dice a massive dataset, and _pandas_ or _SQL_ cannot do the trick - pam pam pam, Spark is here have no fear.

In this post we will go over all the steps needed to spin up a spark cluster, fetch and process data, and finally load the results.

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
- EMR service - Elastic Map Reduce is AWS's managed Hadoop framework.
- S3 service - AWS's storage service. In the solution we present in this post we assume that the raw data is stored on a S3 bucket.
- Boto 3 - Boto is the Amazon Web Services (AWS) SDK for Python. It enables Python developers to create, configure, and manage AWS services.

## Solution formulation

- EMR loader
- Bootstrap
- S3 Connectors
- Processing

## Conclusion

In this tutorial
