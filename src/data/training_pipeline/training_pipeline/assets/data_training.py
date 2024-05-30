import pandas as pd
from dagster import asset, job, op, AssetIn
from feast import FeatureStore
from sqlalchemy import create_engine
from sklearn.preprocessing import OrdinalEncoder
from concurrent.futures import ThreadPoolExecutor
import mlflow
import mlflow.sklearn

from sklearn.decomposition import PCA
from sklearn.preprocessing import RobustScaler
from sklearn.linear_model import LinearRegression, Ridge, Lasso, BayesianRidge, ElasticNet
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split, GridSearchCV

# from data.training_pipeline.training_pipeline.functions.checking import df_description

# Database configuration
mlflow.set_tracking_uri("http://mlflow:5000")

@asset(ins={"df": AssetIn("encoding_applying")})
def training_data(context, df):


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
    context.log.info(f"{result[0]} - Best Params: {result[1]} - RMSE: {result[2]}, R^2: {result[3]}")

  return results
