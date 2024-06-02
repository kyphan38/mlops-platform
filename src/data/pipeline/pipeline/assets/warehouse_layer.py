import pandas as pd
from dagster import asset, AssetIn, Output

from ..utils.checking import df_description

compute_kind = "PostgreSQL"
layer = "warehouse_layer"

# Listing table
@asset(
  name="listing_table",
  key_prefix=["warehouse"],
  ins={"listing_table": AssetIn(key_prefix=["gold"])},
  io_manager_key="psql_io_manager",
  compute_kind=compute_kind,
  group_name=layer,

)
def listing_table(context, listing_table: pd.DataFrame,) -> Output:
  df = listing_table
  df_description(context, df)

  return Output(
    df,
    metadata={
      "table": "listing_table",
      "records count": len(df),
      "columns count": len(df.columns)
    }
  )

# Host table
@asset(
  name="host_table",
  key_prefix=["warehouse"],
  ins={"host_table": AssetIn(key_prefix=["gold"])},
  io_manager_key="psql_io_manager",
  compute_kind=compute_kind,
  group_name=layer,
)
def host_table(context, host_table: pd.DataFrame,) -> Output:
  df = host_table
  df_description(context, df)

  return Output(
    df,
    metadata={
      "table": "host_table",
      "records count": len(df),
      "columns count": len(df.columns)
    }
  )

# Review table
@asset(
  name="review_table",
  key_prefix=["warehouse"],
  ins={"review_table": AssetIn(key_prefix=["gold"])},
  io_manager_key="psql_io_manager",
  compute_kind=compute_kind,
  group_name=layer,
)
def review_table(context, review_table: pd.DataFrame,) -> Output:
  df = review_table
  df_description(context, df)

  return Output(
    df,
    metadata={
      "table": "review_table",
      "records count": len(df),
      "columns count": len(df.columns)
    }
  )

# Fact table
@asset(
  name="fact_table",
  key_prefix=["warehouse"],
  ins={"fact_table": AssetIn(key_prefix=["gold"])},
  io_manager_key="psql_io_manager",
  compute_kind=compute_kind,
  group_name=layer,
)
def fact_table(context, fact_table: pd.DataFrame,) -> Output:
  df = fact_table
  df_description(context, df)

  return Output(
    df,
    metadata={
      "table": "fact_table",
      "records count": len(df),
      "columns count": len(df.columns)
    }
  )
