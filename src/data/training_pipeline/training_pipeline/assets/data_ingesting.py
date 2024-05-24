import pandas as pd
from dagster import asset, op, job
from feast import FeatureStore
from sqlalchemy import create_engine
from concurrent.futures import ThreadPoolExecutor

# from ..functions.checking import df_description
from ..functions.feature_selection import listing_features, host_features, review_features, fact_features

db_config = {
  'user': 'admin',
  'password': 'admin123',
  'host': 'feast_postgres',
  'port': '5432',
  'database': 'feast_postgres'
}

def query_data(engine, query):
  return pd.read_sql(query, engine)

def get_historical_features(fs, entity_df, features):
  return fs.get_historical_features(entity_df=entity_df, features=features).to_df()

@asset()
def ingest_data():
  fs = FeatureStore(repo_path="./feature_repo")

  connection_string = f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"
  engine = create_engine(connection_string)

  queries = {
    'listing': "SELECT id, event_timestamp FROM listing_table",
    'host': "SELECT host_id, event_timestamp FROM host_table",
    'review': "SELECT id, event_timestamp FROM review_table",
    'fact': "SELECT id, event_timestamp FROM fact_table"
  }

  with ThreadPoolExecutor() as executor:
    listing_data, host_data, review_data, fact_data = executor.map(lambda q: query_data(engine, q), queries.values())

  listing_df = get_historical_features(fs, listing_data, listing_features)
  host_df = get_historical_features(fs, host_data, host_features)
  review_df = get_historical_features(fs, review_data, review_features)
  fact_df = get_historical_features(fs, fact_data, fact_features)

  # Drop event_timestamp columns
  for df in [listing_df, host_df, review_df, fact_df]:
    df.drop(columns=['event_timestamp'], inplace=True)

  # Merge dataframes
  df = pd.merge(listing_df, host_df, on="host_id", how="left").drop_duplicates(subset=['id'])
  df = pd.merge(df, review_df, on="id", how="left").drop_duplicates(subset=['id'])
  df = pd.merge(df, fact_df, on="id", how="left").drop_duplicates(subset=['id'])

  print(f"Length listing_df {len(listing_df)}")
  print(f"Length host_df {len(host_df)}")
  print(f"Length review_df {len(review_df)}")
  print(f"Length fact_df {len(fact_df)}")
  print(f"Length df {len(df)}")

  # df_description(df)

  return df
