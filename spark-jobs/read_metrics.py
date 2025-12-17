from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("read-metrics").master("local[*]").getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

print("\n" + "="*70)
print("KET QUA TRAIN RANDOM FOREST - CIFAKE DEEPFAKE DETECTION")
print("="*70)

df = spark.read.parquet("hdfs://namenode:8020/results/cifake_metrics")
df.show(truncate=False)

spark.stop()

