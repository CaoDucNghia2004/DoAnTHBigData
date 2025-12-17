from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, lit


def main() -> None:
    """
    CIFAKE Data Ingestion & Transformation
    =======================================
    Bước 1 trong pipeline theo yêu cầu đề tài:
    - Đọc dữ liệu ảnh từ HDFS (đã được upload từ trước)
    - Thêm cột label (FAKE=1, REAL=0) và split (train/test)
    - Lưu dưới dạng Parquet để các bước sau sử dụng

    Lưu ý: Dataset CIFAKE đã là dữ liệu sạch, chuẩn hóa sẵn (32x32 pixels, JPEG)
    nên KHÔNG cần bước "làm sạch" (cleaning) truyền thống.
    """

    # Tạo SparkSession kết nối tới cluster và bật event logging lên HDFS
    spark = (
        SparkSession.builder.appName("cifake-ingestion")
        .master("spark://spark-master:7077")
        .config("spark.eventLog.enabled", "true")
        .config("spark.eventLog.dir", "hdfs://namenode:8020/spark-logs")
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("WARN")

    # =========================================================================
    # STEP 1: INGESTION - Đọc toàn bộ ảnh CIFAKE từ HDFS
    # =========================================================================
    # Dataset CIFAKE gồm 120,000 ảnh:
    #   - train/FAKE: 50,000 ảnh
    #   - train/REAL: 50,000 ảnh
    #   - test/FAKE:  10,000 ảnh
    #   - test/REAL:  10,000 ảnh

    image_paths = [
        "hdfs://namenode:8020/datasets/cifake/train/FAKE",
        "hdfs://namenode:8020/datasets/cifake/train/REAL",
        "hdfs://namenode:8020/datasets/cifake/test/FAKE",
        "hdfs://namenode:8020/datasets/cifake/test/REAL",
    ]

    # Sử dụng Spark DataFrame API để đọc ảnh (KHÔNG dùng vòng lặp local)
    df = spark.read.format("image").load(image_paths)

    print(f"[INGESTION] Tổng số ảnh đọc được từ HDFS: {df.count()}")

    # =========================================================================
    # TRANSFORMATION - Thêm metadata cần thiết cho pipeline
    # =========================================================================

    # Thêm cột split: train/test dựa trên đường dẫn file
    df = df.withColumn(
        "split",
        when(col("image.origin").contains("/train/"), lit("train")).otherwise(
            lit("test")
        ),
    )

    # Thêm cột label: FAKE -> 1, REAL -> 0 (theo yêu cầu đề tài)
    df = df.withColumn(
        "label",
        when(col("image.origin").contains("/FAKE/"), lit(1))
        .when(col("image.origin").contains("/REAL/"), lit(0))
        .otherwise(lit(-1)),
    )

    # Chọn các cột cần thiết để lưu xuống HDFS
    df_final = df.select("image", "label", "split")

    # In thống kê
    print("[INGESTION] Phân bố dữ liệu:")
    df_final.groupBy("split", "label").count().orderBy("split", "label").show()

    # =========================================================================
    # OUTPUT - Lưu dữ liệu dạng Parquet trên HDFS
    # =========================================================================
    output_path = "hdfs://namenode:8020/processed/cifake_ingested"

    (
        df_final.write.mode("overwrite")
        .option("compression", "snappy")
        .parquet(output_path)
    )

    print(f"[INGESTION] Đã lưu dữ liệu tại: {output_path}")

    spark.stop()


if __name__ == "__main__":
    main()

