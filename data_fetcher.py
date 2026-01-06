import os
import numpy as np
import pandas as pd
from tqdm import tqdm
from PIL import Image

from sentinelhub import (
    SHConfig,
    SentinelHubRequest,
    DataCollection,
    BBox,
    CRS,
    bbox_to_dimensions,
    MimeType,
    MosaickingOrder
)

# =======================
# CONFIGURATION
# =======================

BASE_DIR = r"C:\Users\sameer\Desktop\Satellite_Property_Valuation"
DATA_DIR = os.path.join(BASE_DIR, "data")
IMG_DIR = os.path.join(BASE_DIR, "images")

os.makedirs(IMG_DIR, exist_ok=True)

# OAuth
config = SHConfig()
config.sh_client_id = "118cb3d5-8d27-4a48-b7d1-7b72a79c1ab1"
config.sh_client_secret = "t1QhjhEBIabWDV0Geqh6gocJLZ9Mr0z8"

# Image params
RESOLUTION = 10
IMG_SIZE = 224
MAX_CLOUD = 0.2   # 20%
TIME_RANGE = ("2020-01-01", "2023-12-31")

# =======================
# LOAD DATA (NO RENAMING)
# =======================

train = pd.read_excel(os.path.join(DATA_DIR, "train(1).xlsx"))

# =======================
# EVALSCRIPT (TRUE RGB)
# =======================

evalscript = """
//VERSION=3
function setup() {
  return {
    input: ["B04", "B03", "B02"],
    output: { bands: 3 }
  };
}

function evaluatePixel(sample) {
  return [sample.B04, sample.B03, sample.B02];
}
"""

# =======================
# DOWNLOAD LOOP
# =======================

print("Starting image download...")

saved = 0

for idx, row in tqdm(train.iterrows(), total=len(train)):
    try:
        lat = row["lat"]
        lon = row["long"]

        bbox = BBox(
            bbox=[lon - 0.002, lat - 0.002, lon + 0.002, lat + 0.002],
            crs=CRS.WGS84
        )

        size = bbox_to_dimensions(bbox, resolution=RESOLUTION)

        request = SentinelHubRequest(
            evalscript=evalscript,
            input_data=[
                SentinelHubRequest.input_data(
                    data_collection=DataCollection.SENTINEL2_L2A,
                    time_interval=TIME_RANGE,
                    mosaicking_order=MosaickingOrder.LEAST_CC,
                    maxcc=MAX_CLOUD
                )
            ],
            responses=[
                SentinelHubRequest.output_response("default", MimeType.PNG)
            ],
            bbox=bbox,
            size=size,
            config=config
        )

        img = request.get_data()[0]

        if img.mean() < 5:   # skip empty tiles
            continue

        img = Image.fromarray(img)
        img = img.resize((IMG_SIZE, IMG_SIZE))

        img.save(os.path.join(IMG_DIR, f"{idx}.png"))
        saved += 1

    except Exception:
        continue

print("✅ Image download completed")
print("Total valid images saved:", saved)
