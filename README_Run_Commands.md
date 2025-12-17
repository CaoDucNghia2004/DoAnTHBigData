# Runbook lệnh thực thi pipeline "The Deepfake Hunter" (CIFAKE)

File này ghi lại **các lệnh đã (hoặc sẽ) thực thi thực tế** trong dự án, theo đúng thứ tự các bước trong `PLAN_Pipeline_Steps.txt`.

Mỗi nhóm lệnh gồm:

-   **Tiêu đề / Bước**: Liên kết tới bước trong kế hoạch.
-   **Mục đích**: Lệnh dùng để làm gì.
-   **Lệnh**: Cụ thể đã chạy lệnh nào (trên host hoặc trong container).
-   **Kết quả / Ghi chú**: Kết quả mong đợi, file/thư mục sinh ra, hoặc log quan trọng.

---

## Bước 1 – Khởi động cụm Hadoop + Spark và kiểm tra HDFS

### Lệnh 1.1 – Khởi động cụm Hadoop + Spark (Docker Compose)

-   **Mục đích**: Tạo và khởi động cụm gồm `namenode`, `datanode`, `spark-master`, `spark-worker`, `spark-history-server`.
-   **Thực hiện trên host (PowerShell), tại thư mục project**:
    -   `cwd`: thư mục gốc project `e:\GOCHOCTAPHK1_2025-2026\THBigData\DoAnCuoiKi`.
    -   **Lệnh**:
        -   `cd spark-hadoop; docker-compose up -d`
-   **Kết quả mong đợi**:
    -   Docker pull image `bde2020/spark-history-server:3.3.0-hadoop3.3` (lần đầu chạy).
    -   Các container sau được tạo và đang chạy:
        -   `namenode` (Hadoop NameNode)
        -   `datanode` (Hadoop DataNode)
        -   `spark-master` (Spark Master UI: http://localhost:8080)
        -   `spark-worker` (Spark Worker UI: http://localhost:8081)
        -   `spark-history-server` (Spark History UI: http://localhost:18080)

### Lệnh 1.2 – Tạo thư mục `/tmp` và liệt kê HDFS gốc

-   **Mục đích**: Kiểm tra HDFS hoạt động bằng việc tạo thư mục và liệt kê gốc `/` trên HDFS.
-   **Thực hiện trên host (PowerShell)**:
    -   `cwd`: thư mục gốc project.
    -   **Lệnh**:
        1. `docker exec namenode hdfs dfs -mkdir -p /tmp`
        2. `docker exec namenode hdfs dfs -ls /`
-   **Kết quả mong đợi**:
    -   Lệnh 1 chạy không báo lỗi (nếu `/tmp` chưa tồn tại, sẽ được tạo; nếu đã có rồi thì không sao).
    -   Lệnh 2 hiển thị danh sách gốc HDFS, có thư mục `/tmp`, ví dụ:
        -   `Found 1 items`
        -   `drwxr-xr-x   - root supergroup          0 2025-12-15 07:52 /tmp`

---

## Bước 2 – Chuẩn bị dataset CIFAKE trên máy local

(Sẽ cập nhật khi thực hiện.)

---

## Bước 3 – Upload CIFAKE vào HDFS

(Sẽ cập nhật khi thực hiện.)

---

## Bước 4 – Cấu hình Spark History Server + event logs trên HDFS

(Sẽ cập nhật khi thực hiện.)

---

## Bước 5 – Job ETL đọc ảnh từ HDFS

(Sẽ cập nhật khi thực hiện.)

---

## Bước 6 – Trích xuất đặc trưng bằng ResNet/MobileNet (PyTorch trong Spark)

(Sẽ cập nhật khi thực hiện.)

---

## Bước 7 – Huấn luyện & đánh giá model với Spark MLlib

(Sẽ cập nhật khi thực hiện.)

---

## Bước 8 – Thu thập log & screenshot từ Spark History Server

(Sẽ cập nhật khi thực hiện.)

---

## Bước 9 – Hoàn thiện tài liệu báo cáo & README

(Sẽ cập nhật khi thực hiện.)
