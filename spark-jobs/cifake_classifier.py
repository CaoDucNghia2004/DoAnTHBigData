from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.evaluation import MulticlassClassificationEvaluator


def main() -> None:
    """
    CIFAKE Classification & Evaluation - Random Forest
    ====================================================
    Buoc 3 & 4 trong pipeline theo yeu cau de tai:
    - Doc vector dac trung tu HDFS (da trich xuat bang MobileNetV2)
    - Huan luyen Random Forest Classifier bang Spark MLlib
    - Danh gia model: Accuracy, Precision, Recall, F1-Score
    - Luu ket qua (Business Insight) ve HDFS

    Model: Random Forest voi 100 trees, maxDepth=15 de dat do chinh xac cao nhat
    """

    spark = (
        SparkSession.builder.appName("cifake-randomforest-classification")
        .master("spark://spark-master:7077")
        .config("spark.eventLog.enabled", "true")
        .config("spark.eventLog.dir", "hdfs://namenode:8020/spark-logs")
        .config("spark.executor.memory", "4g")
        .config("spark.driver.memory", "2g")
        .config("spark.executor.memoryOverhead", "1g")
        .config("spark.sql.shuffle.partitions", "20")
        .config("spark.default.parallelism", "20")
        .config("spark.memory.fraction", "0.6")
        .config("spark.memory.storageFraction", "0.3")
        .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer")
        .config("spark.kryoserializer.buffer.max", "512m")
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("WARN")

    print("="*70)
    print("CIFAKE DEEPFAKE DETECTION - RANDOM FOREST CLASSIFIER")
    print("="*70)

    # STEP 3: CLASSIFICATION - Doc features tu buoc Feature Extraction
    print("\n[STEP 1] Dang doc du lieu features tu HDFS...")
    input_path = "hdfs://namenode:8020/processed/cifake_features"
    df = spark.read.parquet(input_path)

    # Cache du lieu de tang toc
    df.cache()
    total_samples = df.count()
    print(f"[INFO] Tong so samples: {total_samples}")

    # Chia train/test dua tren cot split
    train_df = df.filter(col("split") == "train")
    test_df = df.filter(col("split") == "test")

    # Cache train va test
    train_df.cache()
    test_df.cache()

    train_count = train_df.count()
    test_count = test_df.count()

    print(f"[INFO] Train set: {train_count} samples")
    print(f"[INFO] Test set: {test_count} samples")

    # Kiem tra phan bo label
    print("\n[STEP 2] Kiem tra phan bo du lieu:")
    print("Train set:")
    train_df.groupBy("label").count().show()
    print("Test set:")
    test_df.groupBy("label").count().show()

    # TRAIN RANDOM FOREST - Cau hinh toi uu cho do chinh xac cao
    print("\n[STEP 3] Dang train Random Forest Classifier...")
    print("Cau hinh: numTrees=100, maxDepth=15, minInstancesPerNode=2")
    print("Vui long doi, qua trinh nay mat khoang 30-45 phut...")

    rf = RandomForestClassifier(
        featuresCol="features",
        labelCol="label",
        predictionCol="prediction",
        probabilityCol="probability",
        numTrees=100,           # 100 cay de tang do chinh xac
        maxDepth=15,            # Do sau 15 de hoc duoc pattern phuc tap
        minInstancesPerNode=2,  # Giam overfitting
        featureSubsetStrategy="sqrt",  # Chon sqrt(1280) ~ 36 features moi split
        seed=42                 # Reproducible results
    )

    rf_model = rf.fit(train_df)
    print("[INFO] Train hoan tat!")

    # PREDICTION
    print("\n[STEP 4] Dang du doan tren test set...")
    rf_pred = rf_model.transform(test_df)

    # EVALUATION - Tinh cac metrics
    print("\n[STEP 5] Dang danh gia model...")

    evaluator_acc = MulticlassClassificationEvaluator(
        labelCol="label", predictionCol="prediction", metricName="accuracy"
    )
    evaluator_precision = MulticlassClassificationEvaluator(
        labelCol="label", predictionCol="prediction", metricName="weightedPrecision"
    )
    evaluator_recall = MulticlassClassificationEvaluator(
        labelCol="label", predictionCol="prediction", metricName="weightedRecall"
    )
    evaluator_f1 = MulticlassClassificationEvaluator(
        labelCol="label", predictionCol="prediction", metricName="f1"
    )

    accuracy = evaluator_acc.evaluate(rf_pred)
    precision = evaluator_precision.evaluate(rf_pred)
    recall = evaluator_recall.evaluate(rf_pred)
    f1_score = evaluator_f1.evaluate(rf_pred)

    # Tinh Confusion Matrix
    print("\n[STEP 6] Confusion Matrix:")
    rf_pred.groupBy("label", "prediction").count().orderBy("label", "prediction").show()

    # Tinh chi tiet TP, TN, FP, FN
    tp = rf_pred.filter((col("label") == 1) & (col("prediction") == 1)).count()
    tn = rf_pred.filter((col("label") == 0) & (col("prediction") == 0)).count()
    fp = rf_pred.filter((col("label") == 0) & (col("prediction") == 1)).count()
    fn = rf_pred.filter((col("label") == 1) & (col("prediction") == 0)).count()

    # BUSINESS INSIGHT - Ket qua cuoi cung
    print("\n" + "="*70)
    print("BUSINESS INSIGHT - KET QUA DANH GIA MODEL")
    print("="*70)

    print("\n" + "-"*50)
    print("RANDOM FOREST CLASSIFIER (MobileNetV2 Features)")
    print("-"*50)
    print(f"  - So cay (numTrees):     100")
    print(f"  - Do sau toi da:         15")
    print(f"  - Feature vector:        1280 chieu (MobileNetV2)")
    print(f"  - Train samples:         {train_count}")
    print(f"  - Test samples:          {test_count}")

    print("\n" + "-"*50)
    print("KET QUA DANH GIA")
    print("-"*50)
    print(f"  ACCURACY:    {accuracy:.4f}  ({accuracy*100:.2f}%)")
    print(f"  PRECISION:   {precision:.4f}  ({precision*100:.2f}%)")
    print(f"  RECALL:      {recall:.4f}  ({recall*100:.2f}%)")
    print(f"  F1-SCORE:    {f1_score:.4f}  ({f1_score*100:.2f}%)")

    print("\n" + "-"*50)
    print("CONFUSION MATRIX CHI TIET")
    print("-"*50)
    print(f"  True Positive (FAKE predicted FAKE):   {tp}")
    print(f"  True Negative (REAL predicted REAL):   {tn}")
    print(f"  False Positive (REAL predicted FAKE):  {fp}")
    print(f"  False Negative (FAKE predicted REAL):  {fn}")

    # Tra loi cau hoi de tai
    print("\n" + "="*70)
    print("TRA LOI CAU HOI DE TAI")
    print("="*70)
    print("\nCau hoi: Model pretrained tren ImageNet co trich xuat du thong tin")
    print("de phat hien anh Deepfake khong?")
    print("\n" + "-"*50)

    if accuracy >= 0.9:
        print(f"KET QUA: ACCURACY = {accuracy*100:.2f}% (>= 90%)")
        print("\nKET LUAN: CO! Model MobileNetV2 pretrained tren ImageNet")
        print("TRICH XUAT DU thong tin de phat hien anh FAKE voi do chinh xac CAO.")
        print("\nGiai thich:")
        print("- MobileNetV2 da hoc duoc cac dac trung hinh anh tu ImageNet")
        print("- Cac dac trung nay (1280 chieu) chua du thong tin de phan biet")
        print("  anh REAL va anh FAKE (AI-generated)")
        print("- Random Forest phan loai hieu qua dua tren cac dac trung nay")
    elif accuracy >= 0.8:
        print(f"KET QUA: ACCURACY = {accuracy*100:.2f}% (>= 80%)")
        print("\nKET LUAN: CO! Model pretrained ImageNet trich xuat TUONG DOI DU")
        print("thong tin de phat hien Deepfake voi do chinh xac KHA.")
    else:
        print(f"KET QUA: ACCURACY = {accuracy*100:.2f}% (< 80%)")
        print("\nKET LUAN: Model pretrained ImageNet CHUA DU de phat hien Deepfake")
        print("voi do chinh xac cao. Can cai thien them.")

    # OUTPUT - Luu metrics ve HDFS
    print("\n" + "="*70)
    print("LUU KET QUA VE HDFS")
    print("="*70)

    metrics_rows = [
        ("random_forest", float(accuracy), float(precision), float(recall), float(f1_score),
         int(tp), int(tn), int(fp), int(fn), int(train_count), int(test_count))
    ]

    metrics_df = spark.createDataFrame(
        metrics_rows,
        ["model", "accuracy", "precision", "recall", "f1_score",
         "true_positive", "true_negative", "false_positive", "false_negative",
         "train_samples", "test_samples"]
    )

    output_metrics_path = "hdfs://namenode:8020/results/cifake_metrics"
    metrics_df.write.mode("overwrite").parquet(output_metrics_path)
    print(f"[OK] Da luu metrics tai: {output_metrics_path}")

    # Luu predictions de phan tich chi tiet
    output_pred_path = "hdfs://namenode:8020/results/cifake_predictions"
    rf_pred.select("label", "prediction", "probability").write.mode(
        "overwrite"
    ).parquet(output_pred_path)
    print(f"[OK] Da luu predictions tai: {output_pred_path}")

    # Luu model
    model_path = "hdfs://namenode:8020/models/cifake_randomforest"
    rf_model.write().overwrite().save(model_path)
    print(f"[OK] Da luu model tai: {model_path}")

    print("\n" + "="*70)
    print("HOAN TAT PIPELINE CIFAKE DEEPFAKE DETECTION!")
    print("="*70)

    spark.stop()


if __name__ == "__main__":
    main()

