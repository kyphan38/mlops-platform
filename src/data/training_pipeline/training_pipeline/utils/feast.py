import pandas as pd

def query_data(engine, query):
  return pd.read_sql(query, engine)

def get_historical_features(fs, entity_df, features):
  return fs.get_historical_features(entity_df=entity_df, features=features).to_df()
