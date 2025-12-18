"""
CIFAKE Pipeline Verification Script
=====================================
Script kiểm tra kết quả sau mỗi bước trong pipeline.
Chạy script này để xác nhận từng bước đã hoàn thành đúng.

Cách chạy:
    docker exec spark-master /opt/spark/bin/spark-submit \
        --master local[*] \
        /opt/spark/work-dir/spark-jobs/verify_pipeline.py
"""

from pyspark.sql import SparkSession


def main():
    spark = SparkSession.builder \
        .appName("verify-pipeline") \
        .master("local[*]") \
        .getOrCreate()
    
    spark.sparkContext.setLogLevel("ERROR")

    print("\n" + "=" * 70)
    print("KIEM TRA KET QUA PIPELINE CIFAKE DEEPFAKE DETECTION")
    print("=" * 70)

    # =========================================================================
    # BƯỚC 0: Kiểm tra dữ liệu gốc trên HDFS
    # =========================================================================
    print("\n" + "-" * 70)
    print("BUOC 0: KIEM TRA DU LIEU GOC TREN HDFS")
    print("-" * 70)
    
    try:
        # Kiểm tra thư mục datasets/cifake có tồn tại không
        hdfs_path = "hdfs://namenode:8020/datasets/cifake"
        fs = spark._jvm.org.apache.hadoop.fs.FileSystem.get(
            spark._jvm.java.net.URI(hdfs_path),
            spark._jsc.hadoopConfiguration()
        )
        path = spark._jvm.org.apache.hadoop.fs.Path(hdfs_path)
        
        if fs.exists(path):
            print(f"[OK] Thu muc {hdfs_path} TON TAI")
            
            # Đếm số file trong từng thư mục con
            subdirs = [
                "/datasets/cifake/train/FAKE",
                "/datasets/cifake/train/REAL", 
                "/datasets/cifake/test/FAKE",
                "/datasets/cifake/test/REAL"
            ]
            
            total_files = 0
            for subdir in subdirs:
                subpath = spark._jvm.org.apache.hadoop.fs.Path(f"hdfs://namenode:8020{subdir}")
                if fs.exists(subpath):
                    files = fs.listStatus(subpath)
                    count = len([f for f in files if f.isFile()])
                    total_files += count
                    print(f"  - {subdir}: {count} files")
                else:
                    print(f"  - {subdir}: KHONG TON TAI")
            
            print(f"\n  => TONG CONG: {total_files} files")
            if total_files == 120000:
                print("  => [OK] Du 120,000 anh CIFAKE!")
            elif total_files > 0:
                print(f"  => [CANH BAO] Chi co {total_files}/120,000 anh")
            else:
                print("  => [LOI] Khong co anh nao!")
        else:
            print(f"[LOI] Thu muc {hdfs_path} KHONG TON TAI")
            print("      Ban can upload du lieu CIFAKE len HDFS truoc!")
            print("\n      Lenh upload:")
            print("      docker exec namenode hdfs dfs -mkdir -p /datasets/cifake")
            print("      docker exec namenode hdfs dfs -put /data/train /datasets/cifake/")
            print("      docker exec namenode hdfs dfs -put /data/test /datasets/cifake/")
    except Exception as e:
        print(f"[LOI] Khong kiem tra duoc HDFS: {e}")

    # =========================================================================
    # BƯỚC 1: Kiểm tra kết quả Ingestion (cifake_etl.py)
    # =========================================================================
    print("\n" + "-" * 70)
    print("BUOC 1: KIEM TRA KET QUA INGESTION (cifake_etl.py)")
    print("-" * 70)
    print("Output path: hdfs://namenode:8020/processed/cifake_ingested")
    
    try:
        df_ingested = spark.read.parquet("hdfs://namenode:8020/processed/cifake_ingested")
        count = df_ingested.count()
        print(f"\n[OK] Da doc duoc {count} records")
        
        print("\nPhan bo theo split va label:")
        df_ingested.groupBy("split", "label").count().orderBy("split", "label").show()
        
        print("Schema:")
        df_ingested.printSchema()
        
        if count == 120000:
            print("[OK] BUOC 1 HOAN TAT - Du 120,000 anh!")
        else:
            print(f"[CANH BAO] Chi co {count}/120,000 anh")
    except Exception as e:
        print(f"[CHUA CHAY] Buoc 1 chua duoc thuc thi hoac bi loi: {e}")
        print("\nLenh chay buoc 1:")
        print("docker exec spark-master /opt/spark/bin/spark-submit \\")
        print("    --master spark://spark-master:7077 \\")
        print("    /opt/spark/work-dir/spark-jobs/cifake_etl.py")

    # =========================================================================
    # BƯỚC 2: Kiểm tra kết quả Feature Extraction
    # =========================================================================
    print("\n" + "-" * 70)
    print("BUOC 2: KIEM TRA KET QUA FEATURE EXTRACTION (cifake_feature_extraction.py)")
    print("-" * 70)
    print("Output path: hdfs://namenode:8020/processed/cifake_features")
    
    try:
        df_features = spark.read.parquet("hdfs://namenode:8020/processed/cifake_features")
        count = df_features.count()
        print(f"\n[OK] Da doc duoc {count} feature vectors")
        
        print("\nPhan bo theo split va label:")
        df_features.groupBy("split", "label").count().orderBy("split", "label").show()
        
        # Kiểm tra kích thước vector
        first_row = df_features.select("features").first()
        if first_row and first_row.features:
            vec_size = len(first_row.features)
            print(f"Kich thuoc vector dac trung: {vec_size} chieu")
            if vec_size == 1280:
                print("[OK] Dung 1280 chieu (MobileNetV2)!")
        
        if count == 120000:
            print("\n[OK] BUOC 2 HOAN TAT - Du 120,000 vectors!")
        else:
            print(f"\n[CANH BAO] Chi co {count}/120,000 vectors")
    except Exception as e:
        print(f"[CHUA CHAY] Buoc 2 chua duoc thuc thi hoac bi loi: {e}")
        print("\nLenh chay buoc 2:")
        print("docker exec spark-master /opt/spark/bin/spark-submit \\")
        print("    --master spark://spark-master:7077 \\")
        print("    --driver-memory 4g --executor-memory 4g \\")
        print("    /opt/spark/work-dir/spark-jobs/cifake_feature_extraction.py")

    # =========================================================================
    # BƯỚC 3: Kiểm tra kết quả Classification
    # =========================================================================
    print("\n" + "-" * 70)
    print("BUOC 3: KIEM TRA KET QUA CLASSIFICATION (cifake_classifier.py)")
    print("-" * 70)
    
    # Kiểm tra metrics
    print("\n3.1. Metrics:")
    print("Output path: hdfs://namenode:8020/results/cifake_metrics")
    try:
        df_metrics = spark.read.parquet("hdfs://namenode:8020/results/cifake_metrics")
        df_metrics.show(truncate=False)
        
        row = df_metrics.first()
        if row:
            print(f"\n[KET QUA CUOI CUNG]")
            print(f"  - Accuracy:  {row.accuracy:.4f} ({row.accuracy*100:.2f}%)")
            print(f"  - Precision: {row.precision:.4f} ({row.precision*100:.2f}%)")
            print(f"  - Recall:    {row.recall:.4f} ({row.recall*100:.2f}%)")
            print(f"  - F1-Score:  {row.f1_score:.4f} ({row.f1_score*100:.2f}%)")
    except Exception as e:
        print(f"[CHUA CHAY] Metrics chua duoc tao: {e}")
    
    # Kiểm tra predictions
    print("\n3.2. Predictions:")
    print("Output path: hdfs://namenode:8020/results/cifake_predictions")
    try:
        df_pred = spark.read.parquet("hdfs://namenode:8020/results/cifake_predictions")
        print(f"[OK] Da luu {df_pred.count()} predictions")
        print("\nMau 5 dong dau:")
        df_pred.show(5)
    except Exception as e:
        print(f"[CHUA CHAY] Predictions chua duoc tao: {e}")
    
    # Kiểm tra model
    print("\n3.3. Model:")
    print("Output path: hdfs://namenode:8020/models/cifake_randomforest")
    try:
        model_path = "hdfs://namenode:8020/models/cifake_randomforest"
        fs = spark._jvm.org.apache.hadoop.fs.FileSystem.get(
            spark._jvm.java.net.URI(model_path),
            spark._jsc.hadoopConfiguration()
        )
        path = spark._jvm.org.apache.hadoop.fs.Path(model_path)
        if fs.exists(path):
            print("[OK] Model Random Forest da duoc luu!")
        else:
            print("[CHUA CHAY] Model chua duoc luu")
    except Exception as e:
        print(f"[LOI] Khong kiem tra duoc model: {e}")
    
    print("\nLenh chay buoc 3 (neu chua chay):")
    print("docker exec spark-master /opt/spark/bin/spark-submit \\")
    print("    --master spark://spark-master:7077 \\")
    print("    --driver-memory 2g --executor-memory 4g \\")
    print("    /opt/spark/work-dir/spark-jobs/cifake_classifier.py")

    # =========================================================================
    # TỔNG KẾT
    # =========================================================================
    print("\n" + "=" * 70)
    print("TONG KET TRANG THAI PIPELINE")
    print("=" * 70)
    print("""
    BUOC 0: Upload data CIFAKE len HDFS    -> /datasets/cifake/
    BUOC 1: Ingestion (cifake_etl.py)      -> /processed/cifake_ingested
    BUOC 2: Feature Extraction             -> /processed/cifake_features  
    BUOC 3: Classification + Evaluation    -> /results/cifake_metrics
                                           -> /results/cifake_predictions
                                           -> /models/cifake_randomforest
    """)

    spark.stop()


if __name__ == "__main__":
    main()

