import numpy as np
from dagster import asset, AssetIn
from sklearn.metrics import mean_squared_error, r2_score

compute_kind = "Pandas"
layer = "training_layer"

@asset(
  name="model_validation",
  ins={
    "data": AssetIn("data_preparation"),
    "trained_models": AssetIn("model_training")
    },
  compute_kind=compute_kind,
  group_name=layer,
)
def model_validation(context, data, trained_models):
  _, _, _, X_test_scaled, _, y_test = data

  X_test_scaled = np.array(X_test_scaled, copy=True)
  y_test = np.array(y_test, copy=True)

  result = []
  best_model = None
  best_r2 = -float('inf')

  for name, model in trained_models.items():
    pred = model.predict(X_test_scaled)
    rmse = mean_squared_error(y_test, pred, squared=False)
    r2 = r2_score(y_test, pred)
    result.append((name, model, model.get_params(), rmse, r2))

    if r2 > best_r2:
      best_r2 = r2
      best_model_name = name

  context.log.info(result)
  context.log.info(best_model_name)
    
  return result, best_model_name