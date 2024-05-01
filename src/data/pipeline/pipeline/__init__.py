# Load environment value
import os
from dotenv import load_dotenv
load_dotenv()

from dagster import Definitions, load_assets_from_modules

# Import assets
from .assets.bronze_layer import crawl_data

# Import resources
from .resources.minio_io_manager import MinIOIOManager

# from . import assets

# all_assets = load_assets_from_modules([assets])

# defs = Definitions(
#     assets=all_assets,
# )

MINIO_CONFIG = {
  "minio_endpoint_url": os.getenv("MINIO_ENDPOINT_URL"),
  "minio_access_key_id": os.getenv("MINIO_ACCESS_KEY_ID"),
  "minio_secret_access_key": os.getenv("MINIO_SECRET_ACCESS_KEY")
}

defs = Definitions (
  assets=[ crawl_data
  ],
  resources={
    "minio_io_manager": MinIOIOManager(MINIO_CONFIG)
  }
)
