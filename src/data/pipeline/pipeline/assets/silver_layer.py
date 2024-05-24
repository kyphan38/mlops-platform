import pandas as pd
import numpy as np
from datetime import datetime
from dagster import asset, AssetIn, Output

from .bronze_layer import return_dynamic_asset_names
from ..functions.convertion import special_text_into_numeric, boolean_into_numeric, list_string_into_string
from ..functions.imputation import missing_value
from ..functions.outliers import log_transform
from ..functions.checking import df_description

# Define directories and layers for data management
silver_data_dir = "./data/silver"
compute_kind = "Pandas"
layer = "silver_layer"

location_cols = ["id", "latitude", "longitude", "neighbourhood", "neighborhood_overview",
                 "neighbourhood_cleansed", "neighbourhood_group_cleansed",
                 'event_timestamp']

listing_cols = ["id", "host_id", "listing_url", "name", "description",
                "picture_url", "property_type", "room_type", "accommodates", "bathrooms",
                # "bathrooms_text",
                "bedrooms", "beds", "amenities", "price",
                "has_availability", "availability_30", "availability_60", "availability_90", "availability_365",
                "instant_bookable", "license",
                'event_timestamp']

host_cols = ["host_id", "host_url", "host_name", "host_since", "host_location",
            "host_about", "host_response_time", "host_response_rate", "host_acceptance_rate", "host_is_superhost",
            "host_thumbnail_url", "host_picture_url", "host_neighbourhood", "host_listings_count", "host_total_listings_count",
            "host_verifications", "host_has_profile_pic", "host_identity_verified",
            'event_timestamp']

review_cols = ["id", "number_of_reviews", "number_of_reviews_ltm", "number_of_reviews_l30d", "first_review",
              "last_review", "review_scores_rating", "review_scores_accuracy", "review_scores_cleanliness", "review_scores_checkin",
              "review_scores_communication", "review_scores_location", "review_scores_value", "reviews_per_month",
              'event_timestamp']

fact_cols = ["id", "scrape_id", "last_scraped", "calendar_last_scraped", "source",
            "calendar_updated", "minimum_nights", "maximum_nights", "minimum_minimum_nights", "maximum_minimum_nights",
            "minimum_maximum_nights", "maximum_maximum_nights", "minimum_nights_avg_ntm", "maximum_nights_avg_ntm", "calculated_host_listings_count",
            "calculated_host_listings_count_entire_homes", "calculated_host_listings_count_private_rooms", "calculated_host_listings_count_shared_rooms",
            'event_timestamp']


def data_processing(context, df):
  """Processes dataframe to clean and transform data."""

  context.log.info(f"Length of columns: {len(df.columns)}")

  # Add the event timestamp
  df['event_timestamp'] = datetime.now()

  # Processing specific columns
  df["id"] = pd.to_numeric(df["id"], errors="coerce").dropna().astype("int64")
  df["neighbourhood_cleansed"] = df["neighbourhood_cleansed"].astype(str)
  df["price"] = df["price"].astype("str").str.replace("$", "").str.replace(",", "")
  df["price"] = pd.to_numeric(df["price"], errors='coerce')

  # Convertion
  bool_cols = ["host_is_superhost", "host_has_profile_pic", "host_identity_verified", "has_availability", "instant_bookable"]
  str_cols = ["minimum_nights", "minimum_maximum_nights", "maximum_maximum_nights", "availability_365"]
  lst_str_cols = ["host_verifications", "amenities"]

  for col in bool_cols:
    df[col] = boolean_into_numeric(df[col])

  for col in str_cols:
    df[col] = df[col].replace(",", "").astype(float)

  for col in lst_str_cols:
    df[col] = df[col].apply(list_string_into_string)

  # Fill NA with specific case
  df["bathrooms"] = df["bathrooms"].fillna(df["bathrooms_text"].apply(special_text_into_numeric))

  # Drop unnecessary columns
  drop_cols = ["bathrooms_text", ]
  df.drop(columns=drop_cols, axis=1)

  # Missing value
  df = missing_value(df)

  # Outliers
  df = log_transform(df)

  return df

@asset(
  io_manager_key="minio_io_manager",
  ins={name: AssetIn(key_prefix=["bronze"]) for name in return_dynamic_asset_names()},
  key_prefix=["silver"],
  group_name=layer,
  compute_kind=compute_kind,
)
def location_table(context, **dataframes) -> Output:
  df1 = pd.concat(dataframes.values())
  df = data_processing(context, df1)
  df = df[location_cols].drop_duplicates().reset_index(drop=True)
  df_description(context, df)

  return Output(
    df,
    metadata={
      "table": "location_table",
      "records count": len(df),
      "columns count": len(df.columns)
    }
  )

@asset(
  io_manager_key="minio_io_manager",
  ins={name: AssetIn(key_prefix=["bronze"]) for name in return_dynamic_asset_names()},
  key_prefix=["silver"],
  group_name=layer,
  compute_kind=compute_kind,
  deps=[location_table]
)
def listing_table(context, **dataframes) -> Output:
  df = pd.concat(dataframes.values())
  df = data_processing(context, df)
  df = df[listing_cols].drop_duplicates().reset_index(drop=True)
  df_description(context, df)

  return Output(
    df,
    metadata={
      "table": "listing_table",
      "records count": len(df),
      "columns count": len(df.columns)
    }
  )

@asset(
  io_manager_key="minio_io_manager",
  ins={name: AssetIn(key_prefix=["bronze"]) for name in return_dynamic_asset_names()},
  key_prefix=["silver"],
  group_name=layer,
  compute_kind=compute_kind,
  deps=[listing_table]
)
def host_table(context, **dataframes) -> Output:
  df = pd.concat(dataframes.values())
  df = data_processing(context, df)
  df = df[host_cols].drop_duplicates().reset_index(drop=True)
  df_description(context, df)

  return Output(
    df,
    metadata={
      "table": "host_table",
      "records count": len(df),
      "columns count": len(df.columns)
    }
  )

@asset(
  io_manager_key="minio_io_manager",
  ins={name: AssetIn(key_prefix=["bronze"]) for name in return_dynamic_asset_names()},
  key_prefix=["silver"],
  group_name=layer,
  compute_kind=compute_kind,
  deps=[host_table]
)
def review_table(context, **dataframes) -> Output:
  df = pd.concat(dataframes.values())
  df = data_processing(context, df)
  df = df[review_cols].drop_duplicates().reset_index(drop=True)
  df_description(context, df)

  return Output(
    df,
    metadata={
      "table": "review_table",
      "records count": len(df),
      "column count": len(df.columns)
    }
  )

@asset(
  io_manager_key="minio_io_manager",
  ins={name: AssetIn(key_prefix=["bronze"]) for name in return_dynamic_asset_names()},
  key_prefix=["silver"],
  group_name=layer,
  compute_kind=compute_kind,
  deps=[review_table]
)
def fact_table(context, **dataframes) -> Output:
  df = pd.concat(dataframes.values())
  df = data_processing(context, df)
  df = df[fact_cols].drop_duplicates().reset_index(drop=True)
  df_description(context, df)

  return Output(
    df,
    metadata={
      "table": "fact_table",
      "records count": len(df),
      "columns count": len(df.columns)
    }
  )
