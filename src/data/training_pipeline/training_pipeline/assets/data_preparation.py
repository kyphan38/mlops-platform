import pandas as pd
from dagster import asset, AssetIn, AssetOut, multi_asset
from sklearn.preprocessing import RobustScaler
from sklearn.model_selection import train_test_split

from ..utils.model.transforming import yeo_johnson_transforming

compute_kind = "Pandas"
layer = "training_layer"

@asset(
  name="data_preparation",
  ins={"df": AssetIn("data_validation")},
  compute_kind=compute_kind,
  group_name=layer,
)
def data_preparation(context, df):
  # Data dropping
  df.drop(columns=["id", "host_id"], axis=1, inplace=True)

  # Data transforming
  df = yeo_johnson_transforming(df)

  # Data splitting
  features = df.drop("price", axis=1)
  target = df["price"]
  X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.3, random_state=42)

  # Data standardizing
  scaler = RobustScaler()
  X_train_scaled = scaler.fit_transform(X_train)
  X_test_scaled = scaler.transform(X_test)

  context.log.info(X_train_scaled.shape)

  return X_train, X_test, X_train_scaled, X_test_scaled, y_train, y_test
