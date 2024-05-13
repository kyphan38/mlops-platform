from contextlib import contextmanager
import pandas as pd
from dagster import IOManager, OutputContext, InputContext
from sqlalchemy import create_engine
import pyarrow.parquet as pq
import os
from contextlib import contextmanager
from dagster import IOManager, OutputContext, InputContext
from minio import Minio, S3Error


@contextmanager
def connect_psql(config):
  conn_info = (
    f"postgresql+psycopg2://{config['user']}:{config['password']}"
    + f"@{config['host']}:{config['port']}"
    + f"/{config['database']}"
  )

  db_conn = create_engine(conn_info)
  try:
    yield db_conn
  finally:
    db_conn.dispose()

@contextmanager
def connect_minio(config):
  client = Minio(
    endpoint=config.get("minio_endpoint_url"),
    access_key=config.get("minio_access_key_id"),
    secret_key=config.get("minio_secret_access_key"),
    secure=False
  )
  try:
    client.list_buckets()
    yield client
  except S3Error as e:
    print(f"MinIO S3 Error: {e.code} - {e.message}")
    raise
  except Exception as e:
    print(f"Error connecting to MinIO: {e}")
    raise

class PostgreSQLIOManager(IOManager):
  def __init__(self, config):
    self._config = config

  def _get_path(self, context):
    layer, table = context.asset_key.path
    key_name = os.path.join(layer, *context.asset_key.path[1:]) + ".parquet"
    tmp_dir_path = f"/tmp/{layer}/"

    os.makedirs(tmp_dir_path, exist_ok=True)
    tmp_file_path = os.path.join(tmp_dir_path, os.path.basename(key_name))

    return key_name, tmp_file_path, table

  def handle_output(self, context: OutputContext, obj: pd.DataFrame):
    key_name, tmp_file_path, table = self._get_path(context)

    try:
      with connect_psql(self._config) as engine:
        obj.to_sql(table, engine, if_exists="replace", index=False)
        context.log.info("Write to PostgreSQL successfully!")
    except Exception as e:
      context.log.error(f"Error writing to PostgreSQL: {e}")
      raise

    print("Write successfully!")

  def load_input(self, context: InputContext):
    key_name, tmp_file_path = self._get_path(context)

    try:
      bucket_name = self._config.get("minio_bucket")
      with connect_minio(self._config) as client:
        found = client.bucket_exists(bucket_name)
        if not found:
          client.make_bucket(bucket_name)
        else:
          context.log.info(f"Bucket {bucket_name} already exists")
        client.fget_object(bucket_name, key_name, tmp_file_path)
        context.log.info(f"Parquet file downloaded from MinIO at {key_name}")
        return pd.read_parquet(tmp_file_path)
    except Exception as e:
      context.log.error(f"Error during MinIO upload: {e}")
      raise
