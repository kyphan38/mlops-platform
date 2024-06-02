import mlflow
import numpy as np
import pandas as pd
from dagster import asset, AssetIn
from sklearn.linear_model import LinearRegression, Ridge, Lasso, BayesianRidge, ElasticNet
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error, r2_score

compute_kind = "Pandas"
layer = "training_layer"

mlflow.set_tracking_uri("http://mlflow:5000")

@asset(
  name="model_training",
  ins={"data": AssetIn("data_preparation")},
  compute_kind=compute_kind,
  group_name=layer,
)
def model_training(context, data):
  X_train_scaled, _, y_train, _ = data

  X_train_scaled = np.array(X_train_scaled, copy=True)
  y_train = np.array(y_train, copy=True)

  models_and_params = {
    "Linear Regression": LinearRegression(),
    "Ridge Regression": Ridge(alpha=0.001),
    "Lasso Regression": Lasso(alpha=0.0001),
    "Bayesian Ridge Regression": BayesianRidge(alpha_1=1e-6, lambda_1=1e-6),
    "ElasticNet Regression": ElasticNet(alpha=0.01, l1_ratio=0.2),
    "Decision Tree Regression": DecisionTreeRegressor(max_depth=3),
  }

  trained_models = {}
  for name, model in models_and_params.items():
    model.fit(X_train_scaled, y_train)
    trained_models[name] = model

  return trained_models

@asset(
  name="model_validation",
  ins={
    "data": AssetIn("data_preparation"),
    "trained_models": AssetIn("model_training"),
    },
  compute_kind=compute_kind,
  group_name=layer,
)
def model_validation(context, data, trained_models):
  _, X_test_scaled, _, y_test = data

  X_test_scaled = np.array(X_test_scaled, copy=True)
  y_test = np.array(y_test, copy=True)

  res = []
  for name, model in trained_models.items():
    predictions = model.predict(X_test_scaled)
    rmse = mean_squared_error(y_test, predictions, squared=False)
    r2 = r2_score(y_test, predictions)
    res.append((name, model, model.get_params(), rmse, r2))

  context.log.info(res)

  return res

@asset(
  name="model_exporting",
  ins={"res": AssetIn("model_validation")},
  compute_kind=compute_kind,
  group_name=layer,
)
def model_exporting(context, res):
  for name, model, params, rmse, r2 in res:
    with mlflow.start_run(run_name=name):
      mlflow.log_params(params)
      mlflow.log_metric("rmse", rmse)
      mlflow.log_metric("r2", r2)
      mlflow.sklearn.log_model(model, name)
