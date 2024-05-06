from dagster import Definitions
from .assets.bronze_layer import generate_assets
from .assets.silver_layer import location_table, listing_table, host_table, review_table, fact_table
from .resources.minio_io_manager import MinIOIOManager

from dotenv import load_dotenv
import os
load_dotenv()

# Setting default values in case environment variables are missing
MINIO_CONFIG = {
    "minio_endpoint_url": os.getenv("MINIO_ENDPOINT_URL", "minio:9000"),
    "minio_access_key_id": os.getenv("AWS_ACCESS_KEY_ID", "minio"),
    "minio_secret_access_key": os.getenv("AWS_SECRET_ACCESS_KEY", "minio123"),
    "minio_bucket": os.getenv("MINIO_BUCKET", "warehouse")
}

# Initialize definitions with dynamically generated assets
defs = Definitions(
  assets=[location_table, listing_table, host_table, review_table, fact_table] + generate_assets("minio_io_manager"),
  resources={
    "minio_io_manager": MinIOIOManager(MINIO_CONFIG)
  }
)
