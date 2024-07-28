import mlflow
import numpy as np
import pandas as pd
from dagster import asset, AssetIn
from sklearn.linear_model import LinearRegression, Ridge, Lasso, BayesianRidge, ElasticNet
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error, r2_score

compute_kind = "Pandas"
layer = "training_layer"

@asset(
  name="model_training",
  ins={
    "data": AssetIn("data_preparation")
    },
  compute_kind=compute_kind,
  group_name=layer,
)
def model_training(context, data):
  _, _, X_train_scaled, _, y_train, _ = data

  X_train_scaled = np.array(X_train_scaled, copy=True)
  y_train = np.array(y_train, copy=True)

  models_and_params = {
    "Linear Regression": LinearRegression(),
    "Ridge Regression": Ridge(alpha=10),
    "Lasso Regression": Lasso(alpha=0.0001),
    "Bayesian Ridge Regression": BayesianRidge(alpha_1=1e-6, lambda_1=0.0001),
    "ElasticNet Regression": ElasticNet(alpha=0.001, l1_ratio=0.5),
    # "Decision Tree Regression": DecisionTreeRegressor(max_depth=None),
  }

  trained_models = {}
  for name, model in models_and_params.items():
    model.fit(X_train_scaled, y_train)
    trained_models[name] = model

  context.log.info(trained_models)

  return trained_models