from io import BytesIO
from typing import List, Optional
import os

import numpy as np
from PIL import Image
import torch
from torchvision.models import mobilenet_v2, MobileNet_V2_Weights
from torchvision import transforms

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, udf
from pyspark.sql.types import ArrayType, FloatType
from pyspark.ml.linalg import Vectors, VectorUDT


# Global singleton model + transform, sẽ được load lười (lazy) trên từng Spark worker
_model = None
_transform = None


def get_model_and_transform():
    """Load MobileNetV2 pretrained ImageNet và transform chuẩn ImageNet (lazy)."""
    global _model, _transform

    if _model is None:
        # Đảm bảo trong mỗi Spark executor PyTorch chỉ dùng 1 CPU thread
        torch.set_num_threads(1)

        # Đặt thư mục cache cho Torch/TorchVision vào khu vực ghi được
        # (tránh lỗi PermissionError: không ghi được vào /home/spark).
        cache_dir = os.environ.get("TORCH_HOME") or "/opt/spark/work-dir/.torch"
        os.environ["TORCH_HOME"] = cache_dir
        os.makedirs(cache_dir, exist_ok=True)

        # Model pretrained trên ImageNet, đúng yêu cầu đề bài (ví dụ MobileNetV2)
        weights = MobileNet_V2_Weights.IMAGENET1K_V1
        model = mobilenet_v2(weights=weights)

        # Lấy feature vector ở tầng trước classifier (penultimate layer)
        model.classifier = torch.nn.Identity()
        model.eval()
        for p in model.parameters():
            p.requires_grad_(False)

        # Chuẩn hoá đúng chuẩn ImageNet của MobileNet_V2_Weights
        # (bao gồm Resize, CenterCrop, ToTensor, Normalize ...)
        preprocess = weights.transforms()

        _model = model
        _transform = preprocess

    return _model, _transform
def extract_feature_from_row(
    height: int, width: int, n_channels: int, data: bytes
) -> Optional[List[float]]:
    """Nhận thông tin ảnh từ struct `image` và trả về vector đặc trưng.

    Spark `image` datasource lưu `image.data` là raw pixel (không phải file JPEG/PNG).
    Vì vậy ta cần reshape về (H, W, C) rồi mới đưa vào PIL/ImageNet transform.

    Nếu ảnh hỏng / không khớp kích thước thì trả về None để Spark filter bỏ.
    """

    try:
        model, preprocess = get_model_and_transform()

        # Chuyển buffer bytes -> numpy array uint8
        arr = np.frombuffer(data, dtype=np.uint8)
        expected = int(height) * int(width) * int(n_channels)
        if expected <= 0 or arr.size != expected:
            return None

        arr = arr.reshape((int(height), int(width), int(n_channels)))

        # Chuẩn hoá về 3 kênh RGB
        if n_channels == 1:
            arr = np.repeat(arr, 3, axis=2)
        elif n_channels >= 3:
            arr = arr[:, :, :3]

        img = Image.fromarray(arr.astype("uint8"), mode="RGB")
        tensor = preprocess(img).unsqueeze(0)  # [1, 3, 224, 224]

        with torch.no_grad():
            features = model(tensor)  # [1, 1280] với MobileNetV2 (classifier = Identity)

        vec = features.squeeze(0).cpu().numpy().astype("float32")
        return vec.tolist()
    except Exception:
        return None


def main() -> None:
    """
    CIFAKE Feature Extraction với MobileNetV2
    ==========================================
    Bước 2 trong pipeline theo yêu cầu đề tài:
    - Đọc dữ liệu ảnh đã ingestion từ HDFS
    - Trích xuất đặc trưng bằng MobileNetV2 (pretrained ImageNet)
    - Model chạy PHÂN TÁN trong Spark Workers (qua UDF)
    - Lưu vector đặc trưng dạng Parquet

    Lưu ý: Theo yêu cầu đề tài, KHÔNG được dùng model Deepfake Detector có sẵn,
    phải dùng model pretrained ImageNet (ResNet50/MobileNetV2) để trích đặc trưng.
    """

    spark = (
        SparkSession.builder.appName("cifake-feature-extraction-mobilenetv2")
        .master("spark://spark-master:7077")
        .config("spark.eventLog.enabled", "true")
        .config("spark.eventLog.dir", "hdfs://namenode:8020/spark-logs")
        # Giới hạn tài nguyên executor để tránh OOM
        .config("spark.executor.instances", "1")
        .config("spark.executor.cores", "1")
        .config("spark.executor.memory", "2g")
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("WARN")

    # =========================================================================
    # STEP 2: FEATURE EXTRACTION - Đọc dữ liệu từ bước Ingestion
    # =========================================================================
    input_path = "hdfs://namenode:8020/processed/cifake_ingested"
    df = spark.read.parquet(input_path)

    print(f"[FEATURE EXTRACTION] Số ảnh đầu vào: {df.count()}")

    # =========================================================================
    # Trích xuất đặc trưng bằng MobileNetV2 (chạy PHÂN TÁN trên Spark Workers)
    # =========================================================================

    # Định nghĩa UDF PyTorch chạy trên Spark workers
    # Model MobileNetV2 được load lazy trên mỗi worker (AI Phân tán)
    extract_features_udf = udf(
        extract_feature_from_row, ArrayType(FloatType())
    )

    # Chạy UDF trên các trường image để lấy vector đặc trưng 1280 chiều
    df_with_features = df.withColumn(
        "features_array",
        extract_features_udf(
            col("image.height"),
            col("image.width"),
            col("image.nChannels"),
            col("image.data"),
        ),
    )

    # Loại bỏ các bản ghi không trích xuất được đặc trưng (nếu có lỗi)
    df_with_features = df_with_features.filter(col("features_array").isNotNull())

    # Chuyển ArrayType(float) -> VectorUDT để dùng với Spark MLlib
    to_vector_udf = udf(lambda xs: Vectors.dense(xs), VectorUDT())

    df_final = df_with_features.select(
        to_vector_udf(col("features_array")).alias("features"),
        col("label"),
        col("split"),
    )

    print(f"[FEATURE EXTRACTION] Số vector đặc trưng: {df_final.count()}")

    # =========================================================================
    # OUTPUT - Lưu features dạng Parquet trên HDFS
    # =========================================================================
    output_path = "hdfs://namenode:8020/processed/cifake_features"

    (
        df_final.write.mode("overwrite")
        .option("compression", "snappy")
        .parquet(output_path)
    )

    print(f"[FEATURE EXTRACTION] Đã lưu features tại: {output_path}")

    spark.stop()


if __name__ == "__main__":
    main()

