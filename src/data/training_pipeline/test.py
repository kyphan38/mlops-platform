

import pandas as pd
from feast import FeatureStore
from sqlalchemy import create_engine
from sklearn.preprocessing import OrdinalEncoder
from concurrent.futures import ThreadPoolExecutor
import mlflow
import mlflow.sklearn

from data.training_pipeline.training_pipeline.functions.checking import df_description

import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import RobustScaler
from sklearn.linear_model import LinearRegression, Ridge, Lasso, BayesianRidge, ElasticNet
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import PolynomialFeatures

from feature_selection import listing_features, host_features, review_features, fact_features

db_config = {
  'user': 'admin',
  'password': 'admin123',
  'host': 'feast_postgres',
  'port': '5432',
  'database': 'feast_postgres'
}

mlflow.set_tracking_uri("http://mlflow:5000")

def query_data(engine, query):
  return pd.read_sql(query, engine)

def get_historical_features(fs, entity_df, features):
  return fs.get_historical_features(entity_df=entity_df, features=features).to_df()

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

  df_description(df)

  return df

def encoding_applying(df):
  df.drop('property_type', axis=1, inplace=True)
  df.drop('room_type', axis=1, inplace=True)
  df.drop('host_verifications', axis=1, inplace=True)
  df.drop('amenities', axis=1, inplace=True)

  return df

def training_data(df):
  features = df.drop('price', axis=1)
  target = df['price']
  X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.3, random_state=42)

  # Standardizing the data
  scaler = RobustScaler()
  X_train_scaled = scaler.fit_transform(X_train)
  X_test_scaled = scaler.transform(X_test)

  # Initialize models and hyperparameters
  models_and_params = {
    'Linear Regression': (LinearRegression(), {}),
    'Ridge Regression': (Ridge(), {'alpha': [0.001]}),
    'Lasso Regression': (Lasso(), {'alpha': [0.0001]}),
    'Bayesian Ridge Regression': (BayesianRidge(), {'alpha_1': [1e-6], 'lambda_1': [1e-6]}),
    'ElasticNet Regression': (ElasticNet(), {'alpha': [0.001, 0.01], 'l1_ratio': [0.2]}),
    'Decision Tree Regression': (DecisionTreeRegressor(), {'max_depth': [3]}),
  }

  # Conduct hyperparameter tuning for each model
  results = []
  for name, (model, params) in models_and_params.items():
    with mlflow.start_run(run_name=name):
      grid_search = GridSearchCV(model, params, cv=5, scoring='neg_mean_squared_error')
      grid_search.fit(X_train_scaled, y_train)
      best_model = grid_search.best_estimator_
      predictions = best_model.predict(X_test_scaled)
      rmse = mean_squared_error(y_test, predictions, squared=False)
      r2 = r2_score(y_test, predictions)
      results.append((name, grid_search.best_params_, rmse, r2))

      # Log parameters, metrics, and model
      mlflow.log_params(grid_search.best_params_)
      mlflow.log_metric("rmse", rmse)
      mlflow.log_metric("r2", r2)
      mlflow.sklearn.log_model(best_model, name)

  # Print results
  for result in results:
    print(f"{result[0]} - Best Params: {result[1]} - RMSE: {result[2]}, R^2: {result[3]}")

if __name__ == "__main__":
  df = ingest_data()
  df = encoding_applying(df)
  training_data(df)
