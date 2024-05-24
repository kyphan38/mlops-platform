from dagster import job, Definitions
from .assets.data_ingesting import ingest_data
from .assets.data_transforming import encoding_applying
from .assets.data_training import training_data

defs = Definitions(
  assets=[ingest_data, encoding_applying, training_data],
  # resources={
  #   "minio_io_manager": MinIOIOManager(MINIO_CONFIG),
  #   "psql_io_manager": PostgreSQLIOManager(FEAST_POSTGRES_CONFIG)
  # }
)
