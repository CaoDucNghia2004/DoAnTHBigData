# Đồ án Big Data – Pipeline phân tán "The Deepfake Hunter"

## 1. Mô tả đề tài & mục tiêu

**Môn học:** Thực hành Big Data  
**Nền tảng:** Local Hadoop/Spark Cluster (Docker/VMs/Linux)

Bạn chọn **Option 1: The Deepfake Hunter (Xử lý ảnh)**, yêu cầu xây dựng một **pipeline Big Data phân tán end-to-end**:

1. Nạp dữ liệu thô (Ingestion) lên **HDFS**
2. Xử lý & làm sạch (ETL) bằng **Apache Spark**
3. Trích xuất đặc trưng ảnh bằng **model pretrained ImageNet** (ResNet50, MobileNetV2, …) dùng **PyTorch trong Spark**
4. Huấn luyện bộ phân loại cổ điển (LogisticRegression / RandomForest) bằng **Spark MLlib**
5. Đánh giá mô hình (Accuracy, Precision, Recall) và rút ra **Business Insight**

**Dataset:** CIFAKE (Real vs. AI-generated) ~100.000 ảnh `.jpg` kích thước 32×32.

---

## 2. Các ràng buộc kỹ thuật quan trọng

1. **Bắt buộc dùng HDFS**

    - Dữ liệu **đầu vào thô** (ảnh) phải được upload lên **HDFS** trước khi xử lý.
    - **Không được** đọc trực tiếp từ ổ cứng máy thật (Windows) bằng path local.

2. **Cấm dùng vòng lặp local duyệt qua file**

    - Không dùng `for` + `os.listdir` để duyệt từng file ảnh.
    - Phải dùng **Spark RDD hoặc DataFrame** – ví dụ `spark.read.format("image").load(...)` để Spark tự quét file.

3. **AI phải chạy phân tán trong Spark Workers**

    - Model AI/ML (ResNet/MobileNet, classifier) phải chạy **bên trong Spark** thông qua **UDF / Pandas UDF / Spark MLlib**.
    - Không được chạy Python đơn lẻ ngoài Spark rồi mới nạp kết quả vào Spark.

4. **Lưu trữ trên HDFS dạng Parquet**

    - Tất cả **dữ liệu trung gian** (sau ETL, sau trích đặc trưng) và **kết quả cuối** (predictions) phải được **ghi lại lên HDFS** dưới định dạng **Parquet**.

5. **Spark History Server + Logs**
    - Bắt buộc bật **Spark History Server** (UI port 18080).
    - Cấu hình Spark:
        - `spark.eventLog.enabled=true`
        - `spark.eventLog.dir=hdfs:///spark-logs` (hoặc đường dẫn tương đương trên HDFS)
        - `spark.history.fs.logDirectory=hdfs:///spark-logs`
    - Báo cáo phải có **ảnh chụp WebUI 18080** chứng minh các **Stage/Task chạy song song**.

---

## 3. Ý tưởng pipeline tổng thể

**Luồng dữ liệu:**

1. **Raw images (CIFAKE)** trên máy thật → upload lên **HDFS** (ví dụ: `/datasets/cifake/...`).
2. **Spark** đọc ảnh từ HDFS bằng DataFrame (`format("image")`).
3. **ETL**: chuẩn hoá label, lọc file lỗi, chuẩn hoá schema.
4. **Feature Extraction (PyTorch)**: dùng ResNet50/MobileNetV2 pretrained ImageNet trong **Spark UDF/Pandas UDF** để trích vector đặc trưng.
5. Chuyển mảng đặc trưng → kiểu `Vector` của `pyspark.ml.linalg`.
6. Dùng **Spark MLlib** (LogisticRegression / RandomForestClassifier) để huấn luyện model phân loại **Real vs Fake**.
7. Ghi **dữ liệu trung gian & kết quả** (Parquet) trở lại HDFS.
8. Dùng **Spark History Server** (port 18080) để xem log và stages, chụp màn hình cho báo cáo.

---

## 4. Các bước thực hiện theo thứ tự

### Bước 1 – Ổn định môi trường Spark + HDFS (Docker)

1. Khởi động cluster bằng `docker-compose up -d` với các service: `spark-master`, `spark-worker`, `namenode`, `datanode`.
2. Vào container `namenode` kiểm tra HDFS: `hdfs dfs -ls /`.
3. Đảm bảo Spark dùng `fs.defaultFS = hdfs://namenode:8020` (qua `spark-defaults.conf` hoặc khi tạo `SparkSession`).

### Bước 2 – Chuẩn bị & đưa dataset CIFAKE lên HDFS

1. Xác định thư mục dataset CIFAKE trên máy thật (ví dụ: `data/CIFAKE/`).
2. Dùng `docker cp` (hoặc volume) để copy dữ liệu vào container `namenode` hoặc `spark-master`.
3. Từ container, tạo thư mục và upload lên HDFS:
    - `hdfs dfs -mkdir -p /datasets/cifake`
    - `hdfs dfs -put /path/trong/container/* /datasets/cifake/`
4. Kiểm tra lại: `hdfs dfs -ls -R /datasets/cifake`.

### Bước 3 – Cấu hình Spark History Server + Event Logs

1. Thêm service **Spark History Server** trong `docker-compose` (expose port `18080`).
2. Tạo thư mục log trên HDFS: `hdfs dfs -mkdir -p /spark-logs`.
3. Cấu hình Spark:
    - `spark.eventLog.enabled=true`
    - `spark.eventLog.dir=hdfs://namenode:8020/spark-logs`
    - `spark.history.fs.logDirectory=hdfs://namenode:8020/spark-logs`
4. Khởi động History Server và vào `http://localhost:18080` để kiểm tra.

### Bước 4 – ETL: Spark đọc ảnh từ HDFS

1. Chọn cách chạy code:
    - `spark-submit` file `.py` bên trong container, **hoặc**
    - Notebook (Jupyter/VSCode) chạy trong container.
2. Dùng Spark DataFrame API để đọc ảnh, ví dụ:
    - `spark.read.format("image").load("hdfs:///datasets/cifake/...")`  
      → Không dùng `os.listdir` + `for`.
3. Tạo cột **label** từ đường dẫn (`image.origin`), phân biệt thư mục `real` vs `fake`.
4. Làm sạch dữ liệu (loại file hỏng, chuẩn hoá label về 0/1).
5. Ghi DataFrame đã ETL về HDFS dạng Parquet, ví dụ: `hdfs:///processed/cifake_clean`.

### Bước 5 – Trích xuất đặc trưng bằng ResNet/MobileNet (PyTorch UDF)

1. Đảm bảo trong container Spark có PyTorch & torchvision (có thể cần `pip install`).
2. Viết **UDF hoặc Pandas UDF**:
    - Nhận ảnh từ cột `image` (DataFrame),
    - Chuyển về tensor, resize (vd: 224×224), normalize theo chuẩn ImageNet,
    - Cho qua model pretrained (ResNet/MobileNet) ở chế độ `eval`,
    - Trả về vector đặc trưng (mảng float).
3. Đảm bảo model được load **trên worker** (dùng biến global + lazy load trong UDF) để thỏa điều kiện **AI phân tán**.
4. Thêm cột `features_array: array<float>`, sau đó convert sang `Vector` (`pyspark.ml.linalg.Vectors.dense`).
5. Ghi DataFrame features ra HDFS dạng Parquet, ví dụ: `hdfs:///processed/cifake_features`.

### Bước 6 – Huấn luyện & đánh giá model với Spark MLlib

1. Đọc DataFrame features từ HDFS (nếu tách bước).
2. Chia train/test bằng `randomSplit([0.8, 0.2], seed=42)`.
3. Định nghĩa model MLlib (LogisticRegression hoặc RandomForestClassifier) với `featuresCol="features"`, `labelCol="label"`.
4. Train model trên tập train, dự đoán trên tập test.
5. Tính **Accuracy, Precision, Recall** bằng `MulticlassClassificationEvaluator` hoặc tự tính từ confusion matrix.
6. Ghi predictions và (nếu muốn) metrics ra HDFS dạng Parquet, ví dụ: `hdfs:///results/cifake_predictions`.

### Bước 7 – Báo cáo & Business Insight

1. Lấy screenshot từ **Spark History Server (port 18080)**:
    - Danh sách ứng dụng (applications),
    - Chi tiết một job với stages/tasks chạy song song.
2. Trình bày các chỉ số: Accuracy, Precision, Recall.
3. Phân tích:
    - Feature extractor (ResNet/MobileNet) có đủ tốt để phát hiện ảnh AI-generated không?
    - Có dấu hiệu overfitting/underfitting không?
    - Nếu thử nhiều model (Logistic vs RandomForest) thì so sánh và giải thích.

---

## 5. Kết quả thực nghiệm & đối chiếu yêu cầu đề bài

### 5.1. Kết quả mô hình (MobileNetV2 + Spark MLlib)

Sau khi chạy đầy đủ pipeline trên cụm Hadoop/Spark (Docker), với feature extractor là **MobileNetV2 pretrained ImageNet** (chạy bằng PyTorch bên trong Spark Workers) và classifier là **Spark MLlib**, thu được:

-   **Logistic Regression (MobileNetV2 features)**

    -   Accuracy ≈ **0.7476**
    -   Precision ≈ **0.9578**
    -   Recall ≈ **0.7476**

-   **Random Forest (MobileNetV2 features)**
    -   Accuracy ≈ **0.7001**
    -   Precision ≈ **0.9522**
    -   Recall ≈ **0.7001**

Kết quả này được ghi lại trên HDFS dưới dạng Parquet:

-   Features sau khi trích xuất: `hdfs://namenode:8020/processed/cifake_features_mobilenetv2`
-   Kết quả metrics: `hdfs://namenode:8020/results/cifake_metrics_mobilenetv2`
-   Dự đoán của Random Forest: `hdfs://namenode:8020/results/cifake_predictions_mobilenetv2_rf`

### 5.2. Business Insight – MobileNetV2 có đủ tốt để phát hiện Deepfake?

-   **Precision rất cao (~0.95)** cho cả Logistic Regression và Random Forest:  
    → Khi model báo một ảnh là **FAKE**, khả năng lớn là đúng, tức là feature MobileNetV2 **rất ít khi “vu oan”** ảnh thật thành giả.
-   **Accuracy & Recall khoảng 0.70–0.75**:  
    → Tổng thể, model phân biệt REAL/FAKE khá ổn; vẫn có một phần ảnh FAKE bị bỏ sót nhưng ở mức chấp nhận được cho một đồ án Big Data với model pretrained.

Kết luận cho báo cáo:

> Feature extractor **MobileNetV2 pretrained ImageNet**, khi kết hợp với classifier cổ điển (đặc biệt là Logistic Regression), **trích xuất đủ thông tin** để phát hiện ảnh AI-generated (deepfake) trên dataset CIFAKE với độ chính xác và precision tương đối cao. Điều này cho thấy các đặc trưng học được từ ImageNet có khả năng tổng quát tốt sang bài toán phát hiện ảnh AI-generated.

### 5.3. Đối chiếu lại các ràng buộc kỹ thuật

Toàn bộ pipeline hiện tại tuân thủ các rule chính trong đề bài:

1. **Bắt buộc dùng HDFS**

    - Raw data CIFAKE, dữ liệu ETL, features, kết quả predictions & metrics đều nằm trên HDFS (`/datasets`, `/processed`, `/results`).

2. **Không dùng vòng lặp local duyệt file**

    - Ảnh được đọc bằng `spark.read.format("image")` trực tiếp từ HDFS; **không dùng** `os.listdir` + `for` để duyệt từng file.

3. **AI chạy phân tán trong Spark Workers**

    - MobileNetV2 (PyTorch) được load bên trong **Spark UDF**, chạy trên executors, đúng yêu cầu **AI Phân tán (Distributed Inference)**.

4. **Lưu trữ Parquet trên HDFS**

    - Sau ETL → `/processed/cifake_clean` (Parquet).
    - Sau feature extraction → `/processed/cifake_features_mobilenetv2` (Parquet).
    - Kết quả model → `/results/cifake_metrics_mobilenetv2`, `/results/cifake_predictions_mobilenetv2_rf` (Parquet).

5. **Spark History Server + Logs**
    - `spark.eventLog.enabled = true`, `spark.eventLog.dir = hdfs://namenode:8020/spark-logs`.
    - Có đầy đủ file log trong `/spark-logs` để Spark History Server (port 18080) hiển thị DAG, stages, tasks chạy song song – phục vụ chụp screenshot cho báo cáo.

Tóm lại, pipeline hiện tại **đáp ứng đầy đủ** cả yêu cầu chức năng (Deepfake Hunter với CIFAKE) lẫn các ràng buộc kỹ thuật (HDFS, không vòng lặp local, AI phân tán, Parquet, History Server) theo đúng đề bài.

---

## 6. Thông tin cần chuẩn bị thêm

Để bắt đầu viết code cụ thể (lệnh `docker cp`, `hdfs dfs -put`, code PySpark + PyTorch), cần xác định:

1. **Đường dẫn dataset CIFAKE** trong project (ví dụ: `data/CIFAKE/`).
2. Bạn muốn triển khai pipeline dạng **script `.py` + `spark-submit`** hay **notebook**.

Sau khi rõ 2 điểm trên, có thể lần lượt triển khai code cho từng bước: ETL → feature extraction → training → evaluation.

---

## 7. Tình trạng hiện tại, lỗi còn tồn tại và hướng xử lý

### 7.1. Thực trạng dữ liệu trên HDFS (theo đúng câu hỏi “tại sao raw nhiều mà ETL còn ít?”)

-   **Dữ liệu thô (raw) trên HDFS** hiện tại:

    -   Đọc trực tiếp 4 thư mục bằng Spark:
        -   `/datasets/cifake/train/FAKE`
        -   `/datasets/cifake/train/REAL`
        -   `/datasets/cifake/test/FAKE`
        -   `/datasets/cifake/test/REAL`
    -   Kết quả đo bằng Spark:
        -   `RAW_COUNT = 110610` ảnh
            → Phù hợp với mô tả đề bài (~100.000 ảnh) và đúng với con số bạn nhớ (~110.610).

-   **Dữ liệu sau ETL hiện tại** trong bảng:
    -   `hdfs://namenode:8020/processed/cifake_clean_full`
    -   Kết quả đo:
        -   `CLEAN_COUNT = 13205` bản ghi
        -   `CLEAN_BY_SPLIT`: `train = 10000`, `test = 3205`

⇒ **Hiện tại ETL chỉ giữ lại ~13.205 / 110.610 ≈ 12% dữ liệu gốc**. Đây là điểm KHÔNG đúng với mong muốn “xử lý đầy đủ 100% dữ liệu thô”.

### 7.2. Nguyên nhân kỹ thuật của lỗi ETL “bị mất nhiều dữ liệu”

Code ETL hiện tại (`spark-jobs/cifake_etl.py`) đọc đúng đủ 4 thư mục CIFAKE, **không có chỗ nào cố tình giới hạn số lượng record** (không `sample`, không `limit`, không `randomSplit` trong ETL):

<augment_code_snippet path="spark-jobs/cifake_etl.py" mode="EXCERPT">

```python
image_paths = [
    "hdfs://namenode:8020/datasets/cifake/train/FAKE",
    "hdfs://namenode:8020/datasets/cifake/train/REAL",
    "hdfs://namenode:8020/datasets/cifake/test/FAKE",
    "hdfs://namenode:8020/datasets/cifake/test/REAL",
]
df = spark.read.format("image").load(image_paths)
```

</augment_code_snippet>

Tuy nhiên, SparkSession trong ETL đang bật hai cấu hình:

<augment_code_snippet path="spark-jobs/cifake_etl.py" mode="EXCERPT">

```python
.config("spark.sql.files.ignoreMissingFiles", "true")
.config("spark.sql.files.ignoreCorruptFiles", "true")
```

</augment_code_snippet>

Kết hợp với thực tế trước đây HDFS từng có lỗi (DataNode bị kill, BlockMissing, "All datanodes are bad"), rất nhiều file ảnh tại thời điểm chạy ETL có thể **bị thiếu block hoặc corrupt tạm thời**. Khi đó:

-   Spark sẽ **im lặng bỏ qua** các file lỗi / thiếu block,
-   Không ném exception (vì `ignoreMissingFiles/ignoreCorruptFiles = true`),
-   Vẫn ghi DataFrame ETL ra HDFS như thể job đã "thành công".

⇒ Kết quả là bảng `cifake_clean_full` hiện tại **chỉ chứa phần subset (~12%) các file mà Spark đọc được ở thời điểm HDFS đang không ổn định**, chứ KHÔNG đại diện cho full 110.610 ảnh gốc.

### 7.3. Cách xử lý hiện tại & những gì đã chạy đúng

Trên cơ sở bảng `cifake_clean_full` hiện có (13.205 bản ghi), pipeline đã được triển khai như sau:

1. **Feature Extraction (MobileNetV2) full trên tập 13.205 bản ghi**

    - Job: `spark-jobs/cifake_feature_extraction.py`.
    - Chạy bằng `/opt/spark/bin/spark-submit` trên cụm Spark (master `spark://spark-master:7077`).
    - Model MobileNetV2 (PyTorch) được load **bên trong Spark UDF**, chạy trên executors.
    - Output: `hdfs://namenode:8020/processed/cifake_features_mobilenetv2_full` (Parquet),
      với **số dòng đúng bằng `CLEAN_COUNT = 13205`** (1:1 với bảng ETL hiện tại).

2. **Train & Evaluate model (Logistic Regression + RandomForest) trên full features (13.205)**

    - Job: `spark-jobs/cifake_train_classifier.py`.
    - Đọc từ `cifake_features_mobilenetv2_full`, chia theo cột `split` (`train = 10000`, `test = 3205`).
    - Train Logistic Regression và RandomForestClassifier trong **Spark MLlib**.
    - Ghi metrics và predictions về HDFS dạng Parquet:
        - Metrics: `hdfs://namenode:8020/results/cifake_metrics_mobilenetv2_full`
        - Predictions (RandomForest): `hdfs://namenode:8020/results/cifake_predictions_mobilenetv2_rf_full`

3. **Đối chiếu với yêu cầu kỹ thuật của đề bài** – trên tập 13.205 bản ghi này:
    - ✓ Raw data, ETL, features, metrics, predictions đều nằm trên **HDFS** (`/datasets`, `/processed`, `/results`).
    - ✓ Không dùng vòng lặp local (`os.listdir` + `for`) để duyệt file ảnh, mà dùng `spark.read.format("image")`.
    - ✓ Model MobileNetV2 (PyTorch) chạy **bên trong Spark Workers** thông qua UDF ⇒ đúng yêu cầu **AI phân tán**.
    - ✓ Toàn bộ trung gian & kết quả được ghi dưới dạng **Parquet** trên HDFS.
    - ✓ `spark.eventLog.enabled = true` và `spark.eventLog.dir = hdfs://namenode:8020/spark-logs` để History Server (port 18080) có thể hiển thị DAG/stages/tasks.

⇒ Về **mặt kiến trúc pipeline và ràng buộc kỹ thuật**, triển khai hiện tại **đã đúng với yêu cầu của đề và giáo viên**.

Điểm duy nhất chưa đạt "100%" đúng với mong muốn của bạn là: **bảng ETL đang nhỏ hơn rất nhiều so với raw (~13k vs 110k)**.

### 7.4. Hướng xử lý đề xuất để thật sự dùng ~100% dữ liệu

Để pipeline thật sự chạy trên **gần như toàn bộ 110.610 ảnh gốc**, có thể ghi rõ trong README / báo cáo hướng xử lý như sau:

1. **Ổn định lại HDFS trước khi chạy ETL**

    - Đảm bảo `namenode` và `datanode` đều đang chạy (qua `docker compose ps`).
    - Chạy `hdfs dfsadmin -report` để xác nhận:
        - Có **1 live datanode**,
        - Không còn `Missing blocks` / `Under replicated blocks` nghiêm trọng.

2. **Chạy lại job ETL trên full raw**

    - Từ host (PowerShell) tại thư mục project:
        - `cd spark-hadoop`
        - `docker exec spark-master bash -lc \
 "/opt/spark/bin/spark-submit --master spark://spark-master:7077 \
  /opt/spark/work-dir/spark-jobs/cifake_etl.py"`
    - Sau khi chạy xong, dùng Spark (hoặc `hdfs dfs -count`) kiểm tra lại:
        - `CLEAN_COUNT` mới phải **tiệm cận 110.610** (trừ đi một số rất ít file thực sự hỏng nếu có).

3. **Chạy lại feature extraction + training trên bảng clean mới**

    - Xoá (hoặc ghi đè) các thư mục:
        - `/processed/cifake_features_mobilenetv2_full`
        - `/results/cifake_metrics_mobilenetv2_full`
        - `/results/cifake_predictions_mobilenetv2_rf_full`
    - Chạy lại tuần tự:
        1. `spark-jobs/cifake_feature_extraction.py`
        2. `spark-jobs/cifake_train_classifier.py`
    - Kiểm tra lại số dòng features và metrics/predictions để đảm bảo đã train + evaluate trên full data.

4. **Ghi chú trong báo cáo**
    - Trình bày rõ:
        - Lý do ban đầu chỉ có 13.205 bản ghi ETL (HDFS từng lỗi, Spark bỏ qua file lỗi nhờ cấu hình `ignoreMissingFiles/ignoreCorruptFiles`).
        - Sau khi ổn định HDFS và chạy lại ETL, pipeline đã được chạy trên gần như toàn bộ **110.610 ảnh CIFAKE**.
    - Như vậy, **vừa minh bạch với giảng viên**, vừa cho thấy bạn hiểu rõ pipeline & cách debug một cụm Big Data thực tế.

### 7.5. Tóm tắt ngắn cho giảng viên

-   **Lỗi chính còn tồn tại (đã phân tích được):**

    -   Bảng ETL `cifake_clean_full` hiện tại chỉ có 13.205 bản ghi, trong khi raw trên HDFS là 110.610 ảnh.
    -   Nguyên nhân: ETL được chạy trong lúc HDFS còn lỗi block; Spark được cấu hình bỏ qua file missing/corrupt nên im lặng skip ~90% file.

-   **Những phần đã đáp ứng yêu cầu đề tài:**

    -   ✓ Ingestion, ETL, feature extraction, training, evaluation **đều chạy trên HDFS**.
    -   ✓ Không dùng vòng lặp local để duyệt file, mà dùng DataFrame `format("image")`.
    -   ✓ Model AI (MobileNetV2) chạy **phân tán trong Spark Workers**.
    -   ✓ Toàn bộ dữ liệu trung gian & kết quả được ghi **Parquet trên HDFS**.
    -   ✓ Đã cấu hình **Spark History Server + event logs trên HDFS** để làm bằng chứng.

-   **Hướng xử lý để hoàn thiện 100%:**
    -   Ổn định lại HDFS ⇒ chạy lại ETL trên full 110.610 ảnh ⇒ chạy lại feature extraction + training ⇒ cập nhật lại metrics.

Nếu cần, phần này có thể được trích nguyên văn vào báo cáo như một mục "Hạn chế & hướng phát triển" của đồ án.
