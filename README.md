# 🎯 CIFAKE DEEPFAKE DETECTION - KẾT QUẢ THỰC HIỆN

## 📋 TỔNG QUAN DỰ ÁN

| Thông tin | Chi tiết |
|-----------|----------|
| **Đề tài** | The Deepfake Hunter - Phát hiện ảnh AI tạo ra |
| **Dataset** | CIFAKE (Real vs AI-Generated) |
| **Số lượng ảnh** | 120,000 ảnh (32x32 pixels) |
| **Model trích xuất** | MobileNetV2 (pretrained ImageNet) |
| **Model phân loại** | Random Forest (Spark MLlib) |

---

## ✅ CÁC BƯỚC ĐÃ THỰC HIỆN

### BƯỚC 1: Upload dữ liệu lên HDFS ✅

| Thông tin | Chi tiết |
|-----------|----------|
| **Tổng ảnh** | 120,000 files |
| **Train FAKE** | 50,000 ảnh |
| **Train REAL** | 50,000 ảnh |
| **Test FAKE** | 10,000 ảnh |
| **Test REAL** | 10,000 ảnh |

**Xem kết quả tại:**
- UI: http://localhost:9870
- Đường dẫn: `/data/cifake/train/FAKE/`, `/data/cifake/train/REAL/`, `/data/cifake/test/FAKE/`, `/data/cifake/test/REAL/`

---

### BƯỚC 2: Trích xuất đặc trưng (Feature Extraction) ✅

| Thông tin | Chi tiết |
|-----------|----------|
| **Model** | MobileNetV2 (pretrained ImageNet) |
| **Output** | Vector 1280 chiều cho mỗi ảnh |
| **Tổng vectors** | 120,000 vectors |
| **Định dạng lưu** | Parquet |

**Xem kết quả tại:**
- UI: http://localhost:9870
- Đường dẫn HDFS: `/processed/cifake_features/`

---

### BƯỚC 3: Train Random Forest + Test ✅

| Thông tin | Chi tiết |
|-----------|----------|
| **Model** | Random Forest Classifier |
| **Số cây (numTrees)** | 100 |
| **Độ sâu (maxDepth)** | 15 |
| **Train samples** | 100,000 ảnh |
| **Test samples** | 20,000 ảnh |

**Xem kết quả tại:**
- UI: http://localhost:9870
- Model đã lưu: `/models/cifake_randomforest/`
- Metrics: `/results/cifake_metrics/`
- Predictions: `/results/cifake_predictions/`

---

## 📊 KẾT QUẢ ĐÁNH GIÁ MODEL

### Các chỉ số chính:

| Metric | Giá trị | Phần trăm |
|--------|---------|-----------|
| **Accuracy** | 0.8776 | **87.76%** |
| **Precision** | 0.8778 | **87.78%** |
| **Recall** | 0.8776 | **87.76%** |
| **F1-Score** | 0.8775 | **87.75%** |

### Confusion Matrix:

| | Predicted FAKE | Predicted REAL |
|---|:---:|:---:|
| **Actual FAKE** | 8,894 (TP) ✅ | 1,106 (FN) ❌ |
| **Actual REAL** | 1,343 (FP) ❌ | 8,657 (TN) ✅ |

- **Đoán đúng:** 17,551 / 20,000 ảnh
- **Đoán sai:** 2,449 / 20,000 ảnh

---

## 🌐 ĐƯỜNG DẪN XEM KẾT QUẢ TRÊN UI

### 1. HDFS NameNode UI
- **URL:** http://localhost:9870
- **Xem:** Browse Directory → Utilities → Browse the file system

| Thư mục HDFS | Nội dung |
|--------------|----------|
| `/data/cifake/` | 120,000 ảnh gốc |
| `/processed/cifake_features/` | Features đã trích xuất (Parquet) |
| `/results/cifake_metrics/` | Accuracy, Precision, Recall, F1 |
| `/results/cifake_predictions/` | Dự đoán chi tiết |
| `/models/cifake_randomforest/` | Model Random Forest đã train |
| `/spark-logs/` | Event logs |

### 2. Spark Master UI
- **URL:** http://localhost:8080
- **Xem:** Danh sách Workers, Applications đang chạy

### 3. Spark Worker UI
- **URL:** http://localhost:8081
- **Xem:** Executors, Tasks đang chạy

### 4. Spark History Server UI
- **URL:** http://localhost:18080
- **Xem:** Lịch sử các jobs đã chạy, Stages, Tasks song song

---

## 📁 CẤU TRÚC THƯ MỤC HDFS

```
hdfs://namenode:8020/
├── data/
│   └── cifake/
│       ├── train/
│       │   ├── FAKE/     (50,000 ảnh)
│       │   └── REAL/     (50,000 ảnh)
│       └── test/
│           ├── FAKE/     (10,000 ảnh)
│           └── REAL/     (10,000 ảnh)
├── processed/
│   └── cifake_features/  (Parquet - 120,000 vectors 1280D)
├── results/
│   ├── cifake_metrics/   (Accuracy, Precision, Recall, F1)
│   └── cifake_predictions/ (Label, Prediction, Probability)
├── models/
│   └── cifake_randomforest/ (Model đã train)
└── spark-logs/           (Event logs cho History Server)
```

---

## 🔍 LỆNH KIỂM TRA KẾT QUẢ

### Kiểm tra dữ liệu trên HDFS:
```bash
docker exec namenode hdfs dfs -ls /data/cifake/
docker exec namenode hdfs dfs -count /data/cifake/
```

### Kiểm tra features:
```bash
docker exec namenode hdfs dfs -ls /processed/cifake_features/
```

### Kiểm tra kết quả:
```bash
docker exec namenode hdfs dfs -ls /results/
docker exec namenode hdfs dfs -ls /models/
```

---

## 📝 KẾT LUẬN

**Câu hỏi đề tài:** Model pretrained trên ImageNet có trích xuất đủ thông tin để phát hiện Deepfake không?

**Trả lời:** **CÓ!** 

Model MobileNetV2 pretrained trên ImageNet kết hợp với Random Forest Classifier đạt độ chính xác **87.76%**, chứng minh rằng các đặc trưng học được từ ImageNet **ĐỦ** để phân biệt ảnh REAL và FAKE (AI-generated).

---

## 🛠️ CÔNG NGHỆ SỬ DỤNG

| Công nghệ | Mục đích |
|-----------|----------|
| **HDFS** | Lưu trữ phân tán |
| **Apache Spark** | Xử lý phân tán |
| **Spark MLlib** | Train Random Forest |
| **MobileNetV2** | Trích xuất đặc trưng |
| **Docker** | Container hóa hệ thống |
| **Parquet** | Định dạng lưu trữ tối ưu |

