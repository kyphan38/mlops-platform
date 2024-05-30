import pandas as pd
from dagster import asset, AssetIn

from ..utils.checking import df_description

compute_kind = "Pandas"
layer = "training_layer"

@asset(
  name="data_validation",
  ins={"df": AssetIn("data_extraction")},
  compute_kind=compute_kind,
  group_name=layer,
)
def data_validation(context, df):

  if df_description(df)==True:
    context.log.info("Data is valid")
    return df
  else:
    error_message = "Data validation failed: The dataset contains missing values or outliers."
    context.log.error(error_message)
    raise ValueError(error_message)
