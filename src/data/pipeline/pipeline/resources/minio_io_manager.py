from contextlib import contextmanager
from dagster import IOManager, ResourceDefinition, OutputContext, InputContext
from minio import Minio
import os
import pandas as pd

# from typing import Any
# import os
# import pandas as pd
# import pyarrow as pa
# import pyarrow.parquet as pq
# from contextlib import contextmanager
# from dagster import IOManager, , InputContext
# from minio import Minio

@contextmanager
def connect_minio(config):
  client = Minio(
    endpoint=config.get("minio_endpoint_url"),
    access_key=config.get("minio_access_key_id"),
    secret_key=config.get("minio_secret_access_key"),
    secure=False
  )
  try:
    yield client
  except Exception:
    raise

class MinIOIOManager(IOManager):
  def __init__(self, config):
      self.config = config

  def _get_path(self, context):
    # Get layer, schema, table
    layer, schema, table = context.asset_key.path
    key = f"{layer}/{schema}/{table}"
    tmp_dir_path = f"/tmp/{layer}/{schema}"

    os.makedirs(tmp_dir_path, exist_ok=True)

    # key = f"{context.resource_key}/{context.step_key}/{context.output_name}.csv"
    # tmp_file_path = f"/tmp/{key}"
    # os.makedirs(os.path.dirname(tmp_file_path), exist_ok=True)
    # return key, tmp_file_path

  def handle_output(self, context: OutputContext, obj: pd.DataFrame):
    key_name, tmp_file_path = self._get_path(context)
    obj.to_csv(tmp_file_path, index=False)

    with connect_minio(self.config) as client:
      if not client.bucket_exists(self.config["bucket"]):
        client.make_bucket(self.config["bucket"])
      client.fput_object(self.config["bucket"], key_name, tmp_file_path)
    os.remove(tmp_file_path)

  def load_input(self, context: InputContext) -> pd.DataFrame:
    key_name, tmp_file_path = self._get_path(context)
    with connect_minio(self.config) as client:
      client.fget_object(self.config["bucket"], key_name, tmp_file_path)
    return pd.read_csv(tmp_file_path)
