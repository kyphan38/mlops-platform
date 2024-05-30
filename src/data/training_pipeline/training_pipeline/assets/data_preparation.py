import pandas as pd
from dagster import asset, AssetIn

from ..utils.outliers import outliers_handling
from ..utils.encoding import data_encoding

compute_kind = "Pandas"
layer = "training_layer"

@asset(
  name="data_preparation",
  ins={"df": AssetIn("data_validation")},
  compute_kind=compute_kind,
  group_name=layer,
)
def data_preparation(context, df):
  # Outliers handling
  df = outliers_handling(df)

  # Data encoding
  df = data_encoding(df)

  return df
