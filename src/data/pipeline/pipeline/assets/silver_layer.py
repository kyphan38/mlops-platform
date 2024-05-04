import pandas as pd
from dagster import asset, AssetIn, Output

from .bronze_layer import return_dynamic_asset_names

silver_data_dir = "./data/silver"
compute_kind = "Pandas"
layer = "silver_layer"

@asset(
  io_manager_key="minio_io_manager",
  ins={name: AssetIn(key_prefix=["bronze"]) for name in return_dynamic_asset_names()},
  key_prefix=["silver"],
  group_name=layer,
  compute_kind=compute_kind,
)
def airbnb_dataset(context, **dataframes) -> Output:
  df = pd.concat(dataframes.values())
  return Output(
    df,
    metadata={
      "table": "airbnb_dataset",
      "records count": len(df),
    }
  )
