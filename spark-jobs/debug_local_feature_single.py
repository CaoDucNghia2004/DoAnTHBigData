from typing import List, Optional

import os
import numpy as np
from PIL import Image
import torch
from torchvision.models import mobilenet_v2, MobileNet_V2_Weights

from pyspark.sql import SparkSession


_model = None
_transform = None


def get_model_and_transform():
    """Load MobileNetV2 pretrained weights and ImageNet transforms (lazy)."""

    global _model, _transform

    if _model is None:
        # Limit torch to a single CPU thread inside each executor / process
        torch.set_num_threads(1)

        # Ensure Torch cache dir is writable inside the container
        cache_dir = os.environ.get("TORCH_HOME") or "/opt/spark/work-dir/.torch"
        os.environ["TORCH_HOME"] = cache_dir
        os.makedirs(cache_dir, exist_ok=True)

        weights = MobileNet_V2_Weights.IMAGENET1K_V1
        model = mobilenet_v2(weights=weights)

        # Use penultimate layer as feature vector
        model.classifier = torch.nn.Identity()
        model.eval()
        for p in model.parameters():
            p.requires_grad_(False)

        preprocess = weights.transforms()

        _model = model
        _transform = preprocess

    return _model, _transform


def extract_debug(height: int, width: int, n_channels: int, data: bytes) -> Optional[List[float]]:
    """Debug version of feature extractor that prints detailed info and errors."""

    print(
        f"extract_debug: h={height}, w={width}, c={n_channels}, "
        f"data_len={len(data) if data is not None else -1}",
        flush=True,
    )

    try:
        model, preprocess = get_model_and_transform()

        arr = np.frombuffer(data, dtype=np.uint8)
        expected = int(height) * int(width) * int(n_channels)
        print(f"expected={expected}, arr.size={arr.size}", flush=True)

        if expected <= 0 or arr.size != expected:
            print("size mismatch or non-positive expected", flush=True)
            return None

        arr = arr.reshape((int(height), int(width), int(n_channels)))
        print(f"reshaped arr shape={arr.shape}", flush=True)

        if n_channels == 1:
            arr = np.repeat(arr, 3, axis=2)
            print("after repeat to 3 channels, shape=", arr.shape, flush=True)
        elif n_channels >= 3:
            arr = arr[:, :, :3]
            print("after slice to 3 channels, shape=", arr.shape, flush=True)

        img = Image.fromarray(arr.astype("uint8"), mode="RGB")
        tensor = preprocess(img).unsqueeze(0)
        print(f"tensor shape={tensor.shape}", flush=True)

        with torch.no_grad():
            features = model(tensor)

        vec = features.squeeze(0).cpu().numpy().astype("float32")
        print(f"feature vec shape={vec.shape}", flush=True)
        return vec.tolist()

    except Exception as e:  # noqa: BLE001
        import traceback

        print("EXCEPTION in extract_debug:", repr(e), flush=True)
        traceback.print_exc()
        return None


def main() -> None:
    spark = (
        SparkSession.builder.appName("debug-local-feature-single")
        .master("spark://spark-master:7077")
        .config("spark.eventLog.enabled", "true")
        .config("spark.eventLog.dir", "hdfs://namenode:8020/spark-logs")
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("WARN")

    path = "hdfs://namenode:8020/processed/cifake_clean_full"
    df = spark.read.parquet(path).limit(1)
    row = df.collect()[0]
    img = row["image"]

    h = int(img["height"])
    w = int(img["width"])
    c = int(img["nChannels"])
    data = img["data"]

    vec = extract_debug(h, w, c, data)
    if vec is None:
        print("Final result: vec is None", flush=True)
    else:
        print("Final result: feature length =", len(vec), flush=True)

    spark.stop()


if __name__ == "__main__":
    main()
