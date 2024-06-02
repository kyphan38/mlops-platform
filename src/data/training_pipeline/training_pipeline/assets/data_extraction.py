import pandas as pd
import os
from dagster import asset
from feast import FeatureStore
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager

from ..utils.model.feature_vars import listing_features, host_features, review_features, fact_features
from ..utils.model.feast import get_historical_features, query_data

compute_kind = "Feast"
layer = "training_layer"

db_config = {
  "user": "admin",
  "password": "admin123",
  "host": "feast_postgres",
  "port": "5432",
  "database": "feast_postgres"
}

@contextmanager
def db_connection(config: dict) -> Engine:
  connection_string = f"postgresql://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{config['database']}"
  engine = create_engine(connection_string)
  try:
    yield engine
  finally:
    engine.dispose()

@asset(
  name="data_extraction",
  compute_kind=compute_kind,
  group_name=layer,
)
def data_extraction(context):
  fs = FeatureStore(repo_path="./feature_repo")

  queries = {
    "listing": "SELECT id, event_timestamp FROM listing_table",
    "host": "SELECT host_id, event_timestamp FROM host_table",
    "review": "SELECT id, event_timestamp FROM review_table",
    "fact": "SELECT id, event_timestamp FROM fact_table"
  }

  with db_connection(db_config) as engine:
    with ThreadPoolExecutor() as executor:
      listing_data, host_data, review_data, fact_data = executor.map(lambda q: query_data(engine, q), queries.values())

  listing_df = get_historical_features(fs, listing_data, listing_features)
  host_df = get_historical_features(fs, host_data, host_features)
  review_df = get_historical_features(fs, review_data, review_features)
  fact_df = get_historical_features(fs, fact_data, fact_features)

  # Drop event_timestamp columns
  for df in [listing_df, host_df, review_df, fact_df]:
    df.drop(columns=["event_timestamp"], inplace=True)

  # Merge dataframes
  df = pd.merge(listing_df, host_df, on="host_id", how="left").drop_duplicates(subset=["id"])
  df = pd.merge(df, review_df, on="id", how="left").drop_duplicates(subset=["id"])
  df = pd.merge(df, fact_df, on="id", how="left").drop_duplicates(subset=["id"])

  # Save data locally
  # os.makedirs("../data")
  # df.to_csv("../data/dataset.csv", index=False)

  return df
