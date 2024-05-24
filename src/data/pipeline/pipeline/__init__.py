from dagster import Definitions

# Import assets from each layer
from .assets.bronze_layer import generate_assets
from .assets.silver_layer import location_table as silver_location_table, listing_table as silver_listing_table, host_table as silver_host_table, review_table as silver_review_table, fact_table as silver_fact_table
from .assets.gold_layer import listing_table as gold_listing_table, host_table as gold_host_table, review_table as gold_review_table, fact_table as gold_fact_table
from .assets.warehouse_layer import listing_table as wh_listing_table, host_table as wh_host_table, review_table as wh_review_table, fact_table as wh_fact_table

# Import resources
from .resources.minio_io_manager import MinIOIOManager
from .resources.psql_io_manager import PostgreSQLIOManager

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

FEAST_POSTGRES_CONFIG = {
  "host": os.getenv("FEAST_POSTGRES_HOST", "feast_postgres"),
  "port": os.getenv("FEAST_POSTGRES_PORT", "5432"),
  "database": os.getenv("FEAST_POSTGRES_DB", "feast_postgres"),
  "user": os.getenv("FEAST_POSTGRES_USER", "admin"),
  "password": os.getenv("FEAST_POSTGRES_PASSWORD", "admin123"),
}

# Initialize definitions with dynamically generated assets
defs = Definitions(
  assets=generate_assets("minio_io_manager") +
  [silver_location_table, silver_listing_table, silver_host_table, silver_review_table, silver_fact_table] +
  [gold_listing_table, gold_host_table, gold_review_table, gold_fact_table] +
  [wh_listing_table, wh_host_table, wh_review_table, wh_fact_table],
  resources={
    "minio_io_manager": MinIOIOManager(MINIO_CONFIG),
    "psql_io_manager": PostgreSQLIOManager(FEAST_POSTGRES_CONFIG)
  }
)
