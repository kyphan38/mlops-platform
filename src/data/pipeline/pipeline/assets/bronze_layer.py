import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
from dagster import asset, Output

from ..utils.scraping import html_processing

compute_kind = "Pandas"
layer = "bronze_layer"
country_tp = ("United States", )

data_dir = "./data/bronze"
os.makedirs(data_dir, exist_ok=True)

def create_dataset(asset_name, io_manager_key, info):
  dir_ = f"{data_dir}/{asset_name}"

  @asset(
    name=asset_name.replace(".csv", "").replace("-", "_").lower(),
    key_prefix=["bronze"],
    io_manager_key=io_manager_key,
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
  response = requests.get("http://insideairbnb.com/get-the-data")
  html = response.text
  soup = BeautifulSoup(html, "html.parser")
  html_processing(soup, country_tp, data_dir)
  assets = []

  for filename in os.listdir(data_dir):
    if filename.endswith(".csv"):
      asset_name = filename
      info = "Dynamic Asset for CSV data"
      assets.append(create_dataset(asset_name, io_manager_key, info))

  return assets

def return_dynamic_asset_names():
  return [filename.replace(".csv", "").replace("-", "_").lower() for filename in os.listdir(data_dir) if filename.endswith(".csv")]
