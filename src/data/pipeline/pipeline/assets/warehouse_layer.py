from dagster import asset, AssetIn, Output
import pandas as pd

ware_data_dir = "./data/warehouse"
compute_kind = "PostgreSQL"
layer = "warehouse_layer"


@asset(
  io_manager_key="psql_io_manager",
  ins={"listing_table": AssetIn(key_prefix=["gold"])},
  key_prefix=["warehouse"],
  group_name=layer,
  compute_kind=compute_kind,
)
def listing_table(context,
                   listing_table: pd.DataFrame,
                   ) -> Output:

  df = listing_table

  return Output(
    df,
    metadata={
      "table": "location_table",
      "records count": len(df),
      "columns count": len(df.columns)
    }
  )

@asset(
  io_manager_key="psql_io_manager",
  ins={"host_table": AssetIn(key_prefix=["gold"])},
  key_prefix=["warehouse"],
  group_name=layer,
  compute_kind=compute_kind,
)
def host_table(context,
                   host_table: pd.DataFrame,
                   ) -> Output:

  df = host_table

  return Output(
    df,
    metadata={
      "table": "location_table",
      "records count": len(df),
      "columns count": len(df.columns)
    }
  )

@asset(
  io_manager_key="psql_io_manager",
  ins={"review_table": AssetIn(key_prefix=["gold"])},
  key_prefix=["warehouse"],
  group_name=layer,
  compute_kind=compute_kind,
)
def review_table(context,
                   review_table: pd.DataFrame,
                   ) -> Output:

  df = review_table

  return Output(
    df,
    metadata={
      "table": "location_table",
      "records count": len(df),
      "columns count": len(df.columns)
    }
  )

@asset(
  io_manager_key="psql_io_manager",
  ins={"fact_table": AssetIn(key_prefix=["gold"])},
  key_prefix=["warehouse"],
  group_name=layer,
  compute_kind=compute_kind,
)
def fact_table(context,
                   fact_table: pd.DataFrame,
                   ) -> Output:

  df = fact_table

  return Output(
    df,
    metadata={
      "table": "location_table",
      "records count": len(df),
      "columns count": len(df.columns)
    }
  )
