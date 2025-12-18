# 📝 DÀN Ý BÁO CÁO ĐỒ ÁN

## **ĐỀ TÀI: XÂY DỰNG PIPELINE BIG DATA PHÂN TÁN PHÁT HIỆN ẢNH DEEPFAKE**

---

# CHƯƠNG 1: TỔNG QUAN

## 1.1. Đặt vấn đề
- Sự phát triển của AI tạo ảnh giả (Deepfake) ngày càng tinh vi
- Nhu cầu phát hiện ảnh giả trong thời đại số
- Thách thức khi xử lý lượng lớn ảnh (hàng trăm nghìn ảnh)
- Giải pháp: Xây dựng hệ thống Big Data phân tán

## 1.2. Mục tiêu đồ án
- Xây dựng Pipeline Big Data End-to-End phát hiện ảnh Deepfake
- Áp dụng xử lý phân tán với Hadoop HDFS + Apache Spark
- Sử dụng Deep Learning (MobileNetV2) để trích xuất đặc trưng
- Huấn luyện mô hình phân loại với Spark MLlib
- Đánh giá hiệu quả mô hình

## 1.3. Phạm vi đồ án
- Dataset: CIFAKE (120,000 ảnh - Real vs AI-Generated)
- Môi trường: Docker containers (HDFS + Spark cluster)
- Model: MobileNetV2 + Random Forest

## 1.4. Cấu trúc báo cáo
- Chương 1: Tổng quan
- Chương 2: Cơ sở lý thuyết
- Chương 3: Kết quả ứng dụng
- Chương 4: Kết luận

---

# CHƯƠNG 2: CƠ SỞ LÝ THUYẾT

## 2.1. Tổng quan về Big Data

### 2.1.1. Khái niệm Big Data
- Định nghĩa Big Data
- Đặc điểm 5V: Volume, Velocity, Variety, Veracity, Value

### 2.1.2. Kiến trúc hệ thống Big Data
- Kiến trúc Lambda
- Kiến trúc Kappa
- Data Pipeline

## 2.2. Hadoop HDFS

### 2.2.1. Giới thiệu HDFS
- Hadoop Distributed File System là gì?
- Kiến trúc Master-Slave (NameNode, DataNode)

### 2.2.2. Cơ chế hoạt động
- Cách lưu trữ file (chia block 128MB)
- Replication factor
- Fault tolerance

### 2.2.3. Ưu điểm của HDFS
- Lưu trữ dữ liệu lớn
- Khả năng mở rộng
- Chịu lỗi cao

## 2.3. Apache Spark

### 2.3.1. Giới thiệu Apache Spark
- Spark là gì?
- So sánh Spark vs MapReduce
- Kiến trúc Spark (Driver, Executor, Cluster Manager)

### 2.3.2. Spark RDD và DataFrame
- Resilient Distributed Dataset (RDD)
- DataFrame và Dataset
- Lazy evaluation

### 2.3.3. Spark MLlib
- Thư viện Machine Learning của Spark
- Các thuật toán hỗ trợ
- Pipeline ML trong Spark

## 2.4. Deep Learning - MobileNetV2

### 2.4.1. Convolutional Neural Network (CNN)
- Kiến trúc CNN cơ bản
- Convolution, Pooling, Fully Connected

### 2.4.2. Transfer Learning
- Khái niệm Transfer Learning
- Pretrained model trên ImageNet
- Feature Extraction vs Fine-tuning

### 2.4.3. MobileNetV2
- Kiến trúc MobileNetV2
- Depthwise Separable Convolution
- Inverted Residuals
- Output: Vector 1280 chiều

## 2.5. Random Forest Classifier

### 2.5.1. Decision Tree
- Cây quyết định là gì?
- Cách xây dựng cây quyết định

### 2.5.2. Random Forest
- Ensemble Learning
- Bagging (Bootstrap Aggregating)
- Cách Random Forest hoạt động
- Ưu điểm: Giảm overfitting, ổn định

### 2.5.3. Các tham số quan trọng
- numTrees: Số lượng cây
- maxDepth: Độ sâu tối đa
- featureSubsetStrategy: Chiến lược chọn features

## 2.6. Các chỉ số đánh giá mô hình

### 2.6.1. Confusion Matrix
- True Positive (TP), True Negative (TN)
- False Positive (FP), False Negative (FN)

### 2.6.2. Các metrics
- Accuracy = (TP + TN) / Total
- Precision = TP / (TP + FP)
- Recall = TP / (TP + FN)
- F1-Score = 2 * (Precision * Recall) / (Precision + Recall)

---

# CHƯƠNG 3: KẾT QUẢ ỨNG DỤNG

## 3.1. Kiến trúc hệ thống

### 3.1.1. Sơ đồ kiến trúc tổng quan
- Vẽ sơ đồ Pipeline: Ingestion → ETL → ML → Business Insight
- Mô tả luồng dữ liệu

### 3.1.2. Cấu hình Docker containers
- NameNode, DataNode
- Spark Master, Spark Worker
- Spark History Server
- Bảng cấu hình (CPU, RAM, Ports)

## 3.2. Dataset CIFAKE

### 3.2.1. Giới thiệu dataset
- Nguồn: Kaggle - CIFAKE (Real vs AI-Generated)
- Kích thước ảnh: 32x32 pixels
- Tổng số: 120,000 ảnh

### 3.2.2. Phân bố dữ liệu
| Loại | Train | Test | Tổng |
|------|-------|------|------|
| FAKE | 50,000 | 10,000 | 60,000 |
| REAL | 50,000 | 10,000 | 60,000 |
| **Tổng** | **100,000** | **20,000** | **120,000** |

### 3.2.3. Ảnh minh họa
- Ảnh REAL (thật)
- Ảnh FAKE (AI tạo)

## 3.3. Bước 1: Nạp dữ liệu lên HDFS (Ingestion)

### 3.3.1. Mô tả
- Upload 120,000 ảnh từ local lên HDFS
- Cấu trúc thư mục trên HDFS

### 3.3.2. Code thực hiện
- Giải thích code `upload_to_hdfs.py`

### 3.3.3. Kết quả
- Screenshot HDFS UI (http://localhost:9870)
- Đường dẫn: `/data/cifake/`
- Số lượng files đã upload

## 3.4. Bước 2: Trích xuất đặc trưng (Feature Extraction)

### 3.4.1. Mô tả
- Sử dụng MobileNetV2 pretrained trên ImageNet
- Trích xuất vector 1280 chiều cho mỗi ảnh
- Xử lý phân tán với Spark UDF

### 3.4.2. Code thực hiện
- Giải thích code `cifake_feature_extraction.py`
- Spark UDF để chạy MobileNetV2 trên Workers

### 3.4.3. Kết quả
- Screenshot HDFS UI
- Đường dẫn: `/processed/cifake_features/`
- Định dạng: Parquet
- Số lượng vectors: 120,000

## 3.5. Bước 3: Huấn luyện mô hình (Training)

### 3.5.1. Mô tả
- Sử dụng Random Forest Classifier của Spark MLlib
- Cấu hình: numTrees=100, maxDepth=15
- Train trên 100,000 ảnh

### 3.5.2. Code thực hiện
- Giải thích code `cifake_classifier.py`
- Cách khởi tạo RandomForestClassifier
- Cách train model

### 3.5.3. Kết quả
- Screenshot Spark History Server (http://localhost:18080)
- Thời gian train
- Model đã lưu: `/models/cifake_randomforest/`

## 3.6. Bước 4: Đánh giá mô hình (Evaluation)

### 3.6.1. Kết quả trên tập Test (20,000 ảnh)

| Metric | Giá trị |
|--------|---------|
| **Accuracy** | 87.76% |
| **Precision** | 87.78% |
| **Recall** | 87.76% |
| **F1-Score** | 87.75% |

### 3.6.2. Confusion Matrix

| | Predicted FAKE | Predicted REAL |
|---|:---:|:---:|
| **Actual FAKE** | 8,894 (TP) | 1,106 (FN) |
| **Actual REAL** | 1,343 (FP) | 8,657 (TN) |

### 3.6.3. Phân tích kết quả
- Đoán đúng: 17,551 / 20,000 (87.76%)
- Đoán sai: 2,449 / 20,000 (12.24%)
- Model phát hiện FAKE tốt hơn REAL một chút

## 3.7. Bằng chứng xử lý phân tán

### 3.7.1. Spark History Server
- Screenshot danh sách Applications
- Screenshot Stages/Tasks chạy song song
- Screenshot Timeline

### 3.7.2. HDFS UI
- Screenshot cấu trúc thư mục
- Screenshot dữ liệu đã lưu

---

# CHƯƠNG 4: KẾT LUẬN

## 4.1. Kết quả đạt được

### 4.1.1. Về kỹ thuật
- Xây dựng thành công Pipeline Big Data phân tán
- Tích hợp HDFS + Spark + Deep Learning
- Xử lý 120,000 ảnh với hệ thống phân tán

### 4.1.2. Về mô hình
- Accuracy đạt 87.76% - mức khá tốt
- Model MobileNetV2 trích xuất đủ thông tin để phát hiện Deepfake
- Random Forest phân loại hiệu quả

## 4.2. Trả lời câu hỏi đề tài

**Câu hỏi:** Model pretrained trên ImageNet có trích xuất đủ thông tin để phát hiện Deepfake không?

**Trả lời:** **CÓ!** Model MobileNetV2 pretrained trên ImageNet kết hợp với Random Forest đạt độ chính xác 87.76%, chứng minh rằng các đặc trưng học được từ ImageNet ĐỦ để phân biệt ảnh REAL và FAKE.

## 4.3. Hạn chế

- Ảnh kích thước nhỏ (32x32) - chưa thử với ảnh lớn hơn
- Chỉ dùng 1 Worker - có thể scale thêm
- Chưa thử các model khác (ResNet50, EfficientNet)

## 4.4. Hướng phát triển

- Thử với dataset ảnh lớn hơn (256x256, 512x512)
- Thêm nhiều Workers để tăng tốc độ xử lý
- Thử các model khác: ResNet50, EfficientNet
- Xây dựng API để detect ảnh real-time
- Deploy lên cloud (AWS EMR, Google Dataproc)

---

# PHỤ LỤC

## A. Hướng dẫn cài đặt và chạy
- Tham khảo file `HUONG_DAN_THUC_THI.md`

## B. Source code
- `upload_to_hdfs.py` - Upload dữ liệu
- `cifake_feature_extraction.py` - Trích xuất đặc trưng
- `cifake_classifier.py` - Train và đánh giá model
- `read_metrics.py` - Đọc kết quả

## C. Cấu hình Docker
- `docker-compose.yml`
- `Dockerfile.spark-pytorch`

---

# TÀI LIỆU THAM KHẢO

1. Apache Spark Documentation - https://spark.apache.org/docs/latest/
2. Hadoop HDFS Documentation - https://hadoop.apache.org/docs/
3. MobileNetV2 Paper - Sandler et al., 2018
4. CIFAKE Dataset - Kaggle
5. Random Forest - Breiman, 2001

