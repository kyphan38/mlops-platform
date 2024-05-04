import os
import pandas as pd
import requests
import gzip
import shutil
from bs4 import BeautifulSoup
from datetime import datetime
from dagster import asset, Output, AssetsDefinition

data_dir = "./data/bronze"
compute_kind = "Pandas"
layer = "bronze_layer"

def create_dataset(asset_name, io_manager_key, info):
  dir_ = f"{data_dir}/{asset_name}"

  @asset(
    name = asset_name.replace('.csv', '').replace("-", "_").lower(),
    io_manager_key=io_manager_key,
    key_prefix=["bronze"],
    compute_kind=compute_kind,
    group_name=layer,
  )
  def dataset(context):
    df = pd.read_csv(dir_)
    return Output(
      df,
      metadata={
        "directory": dir_,
        "info": info
      }
    )

  return dataset

def generate_assets(io_manager_key):
  assets = []

  for filename in os.listdir(data_dir):
    if filename.endswith(".csv"):
      asset_name = filename
      info = "Dynamic Asset for CSV data"
      assets.append(create_dataset(asset_name, io_manager_key, info))
  return assets

def return_dynamic_asset_names():
  return [filename.replace(".csv", "").replace("-", "_").lower() for filename in os.listdir(data_dir) if filename.endswith(".csv")]
