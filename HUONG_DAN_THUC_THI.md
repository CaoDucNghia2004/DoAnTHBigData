# 🚀 HƯỚNG DẪN THỰC THI PIPELINE CIFAKE DEEPFAKE DETECTION

## 📋 Tổng quan Pipeline

```
Bước 1: Upload ảnh lên HDFS
Bước 2: Trích xuất đặc trưng (MobileNetV2)
Bước 3: Train Random Forest + Test + Đánh giá
```

---

## 🔧 BƯỚC 0: KHỞI ĐỘNG HỆ THỐNG

### 0.1. Khởi động tất cả Docker containers

```bash
docker-compose up -d
```

### 0.2. Kiểm tra containers đang chạy

```bash
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

**Kết quả mong đợi:** 5 containers đang chạy

-   namenode (port 9870)
-   datanode
-   spark-master (port 7077, 8080)
-   spark-worker (port 8081)
-   spark-history-server (port 18080)

### 0.3. Tạo thư mục trên HDFS

```bash
docker exec namenode hdfs dfs -mkdir -p /data/cifake
docker exec namenode hdfs dfs -mkdir -p /processed
docker exec namenode hdfs dfs -mkdir -p /results
docker exec namenode hdfs dfs -mkdir -p /models
docker exec namenode hdfs dfs -mkdir -p /spark-logs
```

---

## 📤 BƯỚC 1: UPLOAD ẢNH LÊN HDFS (Ingestion)

### 1.1. Copy script upload vào spark-master

```bash
docker cp spark-jobs/upload_to_hdfs.py spark-master:/opt/spark/work-dir/
```

### 1.2. Chạy upload ảnh lên HDFS

```bash
docker exec spark-master python /opt/spark/work-dir/upload_to_hdfs.py
```

**Thời gian:** ~10-15 phút (120,000 ảnh)

### 1.3. Kiểm tra ảnh đã upload

```bash
docker exec namenode hdfs dfs -ls /data/cifake/
docker exec namenode hdfs dfs -count /data/cifake/
```

**Kết quả mong đợi:** 120,000 files trên HDFS

---

## 🔍 BƯỚC 2: TRÍCH XUẤT ĐẶC TRƯNG (Feature Extraction)

### 2.1. Copy script feature extraction vào spark-master

```bash
docker cp spark-jobs/cifake_feature_extraction.py spark-master:/opt/spark/work-dir/
```

### 2.2. Chạy trích xuất đặc trưng với MobileNetV2

```bash
docker exec spark-master /opt/spark/bin/spark-submit \
    --master spark://spark-master:7077 \
    --deploy-mode client \
    --driver-memory 4g \
    --executor-memory 4g \
    --executor-cores 2 \
    --conf spark.executor.memoryOverhead=2g \
    /opt/spark/work-dir/cifake_feature_extraction.py
```

**Thời gian:** ~60-90 phút (xử lý 120,000 ảnh qua MobileNetV2)

### 2.3. Kiểm tra features đã trích xuất

```bash
docker exec namenode hdfs dfs -ls /processed/cifake_features/
```

**Kết quả:** File parquet chứa 120,000 vectors (mỗi vector 1280 chiều)

---

## 🤖 BƯỚC 3: TRAIN RANDOM FOREST + TEST + ĐÁNH GIÁ

### 3.1. Copy script classifier vào spark-master

```bash
docker cp spark-jobs/cifake_classifier.py spark-master:/opt/spark/work-dir/
```

### 3.2. Chạy train và đánh giá model

```bash
docker exec spark-master /opt/spark/bin/spark-submit \
    --master spark://spark-master:7077 \
    --deploy-mode client \
    --driver-memory 2g \
    --executor-memory 4g \
    --executor-cores 4 \
    --conf spark.executor.memoryOverhead=1g \
    --conf spark.sql.shuffle.partitions=20 \
    /opt/spark/work-dir/cifake_classifier.py
```

**Thời gian:** ~30-45 phút

-   Train: 100,000 ảnh
-   Test: 20,000 ảnh

### 3.3. Kiểm tra kết quả

```bash
docker exec namenode hdfs dfs -ls /results/
docker exec namenode hdfs dfs -ls /models/
```

**Kết quả:**

-   `/results/cifake_metrics` - Accuracy, Precision, Recall, F1
-   `/results/cifake_predictions` - Dự đoán chi tiết
-   `/models/cifake_randomforest` - Model đã train

---

## 📊 BƯỚC 4: XEM KẾT QUẢ (Business Insight)

### 4.1. Copy script đọc metrics

```bash
docker cp spark-jobs/read_metrics.py spark-master:/opt/spark/work-dir/
```

### 4.2. Xem kết quả đánh giá model

```bash
docker exec spark-master /opt/spark/bin/spark-submit \
    --master local[*] \
    --driver-memory 1g \
    /opt/spark/work-dir/read_metrics.py
```

**Kết quả mong đợi:**

```
+-------------+--------+-----------+--------+----------+
|model        |accuracy|precision  |recall  |f1_score  |
+-------------+--------+-----------+--------+----------+
|random_forest|0.8776  |0.8778     |0.8776  |0.8775    |
+-------------+--------+-----------+--------+----------+
```

---

## 🌐 BƯỚC 5: XEM SPARK HISTORY SERVER (Bằng chứng)

### 5.1. Mở trình duyệt truy cập

```
http://localhost:18080
```

### 5.2. Chụp màn hình các mục sau để báo cáo:

-   Danh sách Applications đã chạy
-   Stages/Tasks chạy song song
-   Timeline của job

---

## 🛑 DỪNG HỆ THỐNG

### Dừng tất cả containers

```bash
docker-compose down
```

### Dừng và xóa dữ liệu (cẩn thận!)

```bash
docker-compose down -v
```

---

## 📁 CẤU TRÚC THƯ MỤC HDFS

```
/data/cifake/
├── train/
│   ├── FAKE/     (50,000 ảnh)
│   └── REAL/     (50,000 ảnh)
└── test/
    ├── FAKE/     (10,000 ảnh)
    └── REAL/     (10,000 ảnh)

/processed/
└── cifake_features/    (Parquet - 120,000 vectors)

/results/
├── cifake_metrics/     (Accuracy, Precision, Recall)
└── cifake_predictions/ (Dự đoán chi tiết)

/models/
└── cifake_randomforest/ (Model đã train)

/spark-logs/            (Event logs cho History Server)
```

---

## ⚠️ XỬ LÝ LỖI THƯỜNG GẶP

### Lỗi 1: Container không khởi động

```bash
docker-compose down
docker-compose up -d
```

### Lỗi 2: HDFS không kết nối được

```bash
docker restart namenode datanode
# Đợi 30 giây
docker exec namenode hdfs dfs -ls /
```

### Lỗi 3: Spark job bị kill do thiếu memory

-   Giảm `--executor-memory` xuống 2g
-   Giảm `--driver-memory` xuống 1g

### Lỗi 4: History Server không hiển thị

```bash
docker restart spark-history-server
# Đợi 10 giây rồi truy cập http://localhost:18080
```

---

## 📈 KẾT QUẢ ĐẠT ĐƯỢC

| Metric        | Giá trị |
| ------------- | ------- |
| **Accuracy**  | 87.76%  |
| **Precision** | 87.78%  |
| **Recall**    | 87.76%  |
| **F1-Score**  | 87.75%  |

**Kết luận:** Model MobileNetV2 + Random Forest có thể phát hiện ảnh Deepfake với độ chính xác ~88%

docker exec spark-master /opt/spark/bin/spark-submit \
 --master local[*] \
 /opt/spark/work-dir/spark-jobs/verify_pipeline.py

docker exec spark-master /opt/spark/bin/spark-submit --master local[*] /opt/spark/work-dir/spark-jobs/verify_pipeline.py
