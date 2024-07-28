# import mlflow
# from dagster import asset, AssetIn
# from sklearn.tree import DecisionTreeRegressor
# from sklearn.metrics import mean_squared_error, r2_score

# from mlflow.models.signature import ModelSignature
# from mlflow.types.schema import Schema
# from mlflow.types.schema import ParamSchema
# from mlflow.types.schema import ParamSpec
# from mlflow.types.schema import ColSpec

# from ..utils.mlflow.creating import create_mlflow_experiment

# compute_kind = "Pandas"
# layer = "training_layer"

# def model_signature_definition(X_train):
#   cols_spec = []
#   data_map = {
#     "int64": "integer",
#     "float64": "double",
#     "bool": "boolean",
#     "str": "string",
#     "object": "string",
#     "date": "datetime",
#   }
#   for name, dtype in X_train.dtypes.to_dict().items():
#     cols_spec.append(ColSpec(name=name, type=data_map[str(dtype)]))
    
#   input_schema = Schema(inputs=cols_spec)
#   output_schema = Schema([ColSpec(name="price", type="double")])
#   param = ParamSpec(name="model_name", dtype="string", default="model1")
#   param_schema = ParamSchema(params=[param])

#   model_signature = ModelSignature(inputs=input_schema, outputs=output_schema, params=param_schema)

#   return model_signature

# @asset(
#   name="model_exporting",
#   ins={
#     "data": AssetIn("data_preparation"),
#     "model_info": AssetIn("model_validation"),
#     },
#   compute_kind=compute_kind,
#   group_name=layer,
# )
# def model_exporting(context, data, model_info):
#   X_train, _, _, _, _, _ = data
#   model_signature = model_signature_definition(X_train)
 
#   result, best_model_name = model_info

#   mlflow.set_tracking_uri("http://mlflow:5000")
#   experiment_id = create_mlflow_experiment(
#     context,
#     experiment_name="model_development",
#     artifact_location="s3://artifacts"
#   )
#   best_model = None
#   best_r2 = -float("inf")

#   with mlflow.start_run("model_experiment", experiment_id=experiment_id) as run:
#     for name, model, params, rmse, r2 in result:
#       with mlflow.start_run(run_name=name, nested=True) as nested_run: 
#         mlflow.log_params(params)
#         mlflow.log_metric("rmse", rmse)
#         mlflow.log_metric("r2", r2)

#         if name == best_model_name:
#           best_model_run_id = nested_run.info.run_id
#           mlflow.sklearn.log_model(model, artifact_path=name, signature=model_signature, registered_model_name=name)
#           context.log.info(f"The best model is: {name}")
#           context.log.info(f"run_id of best_model: {best_model_run_id}")

#     context.log.info(f"run_id of models: {run.info.run_id}")

#   return best_model_run_id

import mlflow
import numpy as np
import pandas as pd
from dagster import asset, AssetIn
from sklearn.linear_model import LinearRegression, Ridge, Lasso, BayesianRidge, ElasticNet
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error, r2_score
from mlflow.exceptions import MlflowException

from mlflow.models.signature import ModelSignature
from mlflow.types.schema import Schema
from mlflow.types.schema import ParamSchema
from mlflow.types.schema import ParamSpec
from mlflow.types.schema import ColSpec

compute_kind = "Pandas"
layer = "training_layer"

def model_signature_definition(X_train):
  cols_spec = []
  data_map = {
    "int64": "integer",
    "float64": "double",
    "bool": "boolean",
    "str": "string",
    "object": "string",
    "date": "datetime",
  }
  for name, dtype in X_train.dtypes.to_dict().items():
    cols_spec.append(ColSpec(name=name, type=data_map[str(dtype)]))
    
  input_schema = Schema(inputs=cols_spec)
  output_schema = Schema([ColSpec(name="price", type="double")])
  param = ParamSpec(name="model_name", dtype="string", default="model1")
  param_schema = ParamSchema(params=[param])

  model_sig = ModelSignature(inputs=input_schema, outputs=output_schema, params=param_schema)

  return model_sig

def create_mlflow_experiment(context, experiment_name, artifact_location):
  try:
    experiment_id= mlflow.create_experiment(
      name=experiment_name,
      artifact_location=artifact_location
    )
  except MlflowException:
    context.log.info(f"Experiment {experiment_name} already exists.")
    experiment_id = mlflow.get_experiment_by_name(experiment_name).experiment_id

  mlflow.set_experiment(experiment_name=experiment_name)

  return experiment_id

@asset(
  name="model_exporting",
  ins={
    "data": AssetIn("data_preparation"),
    "model_info": AssetIn("model_validation"),
  },
  compute_kind=compute_kind,
  group_name=layer,
)
def model_exporting(context, data, model_info):
  X_train, _, _, _, _, _ = data
  model_sig = model_signature_definition(X_train)

  res, best_model_name = model_info

  # Debug: Check model info
  context.log.info(f"Model info: {model_info}")
  context.log.info(f"Results: {res}, Best Model: {best_model_name}")

  mlflow.set_tracking_uri("http://mlflow:5000")

  experiment_id = create_mlflow_experiment(
    context,
    experiment_name="model_development",
    artifact_location="s3://artifacts"
  )

  best_model = None
  best_r2 = -float("inf")

  with mlflow.start_run(run_name="model_experiment", experiment_id=experiment_id) as run:
    for name, model, params, rmse, r2 in res:
      with mlflow.start_run(run_name=name, nested=True) as nested_run: 
        mlflow.log_params(params)
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("r2", r2)

        if name == best_model_name:
          best_model_run_id = nested_run.info.run_id
          mlflow.sklearn.log_model(model, artifact_path=name, signature=model_sig, registered_model_name=name)
          context.log.info(f"The best model is: {name}")
          context.log.info(f"run_id of best_model: {best_model_run_id}")

    context.log.info(f"run_id of models: {run.info.run_id}")

  return best_model_run_id
