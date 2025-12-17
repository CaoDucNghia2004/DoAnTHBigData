#!/bin/bash

# Custom entrypoint for Spark History Server in this project.
# This overrides the default /history-server.sh in the Docker image
# so that the history server reads its event logs from HDFS instead of
# the local filesystem.

export SPARK_HOME=/spark

. "/spark/sbin/spark-config.sh"
. "/spark/bin/load-spark-env.sh"

SPARK_HS_LOG_DIR=$SPARK_HOME/spark-hs-logs
mkdir -p "$SPARK_HS_LOG_DIR"
LOG="$SPARK_HS_LOG_DIR/spark-hs.out"

# Redirect Spark History Server stdout to container stdout
ln -sf /dev/stdout "$LOG"

# IMPORTANT: point Spark History Server to HDFS log directory
# We use the same HDFS path documented in README_DeepfakeHunter_Pipeline.md:
#   hdfs://namenode:8020/spark-logs
# UI port remains 18081 inside container (mapped to 18080 on host).
export SPARK_HISTORY_OPTS="-Dspark.history.fs.logDirectory=hdfs://namenode:8020/spark-logs -Dspark.history.ui.port=18081"

cd /spark/bin && /spark/sbin/../bin/spark-class org.apache.spark.deploy.history.HistoryServer >> "$LOG"
