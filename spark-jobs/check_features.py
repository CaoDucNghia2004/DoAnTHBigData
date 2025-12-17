from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark = SparkSession.builder.appName("check-features").master("local[*]").getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

df = spark.read.parquet("hdfs://namenode:8020/processed/cifake_features")

total = df.count()
print(f"\n=== KIEM TRA FEATURE EXTRACTION ===")
print(f"Tong so samples: {total}")

print(f"\nPhan bo theo split va label:")
df.groupBy("split", "label").count().orderBy("split", "label").show()

print(f"\nKich thuoc vector dac trung:")
first_row = df.select("features").first()
if first_row:
    print(f"Vector size: {len(first_row.features)}")

spark.stop()

