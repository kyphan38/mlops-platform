import pandas as pd
import numpy as np
from dagster import asset, AssetIn, Output

from .bronze_layer import return_dynamic_asset_names

# Define directories and layers for data management
silver_data_dir = "./data/silver"
compute_kind = "Pandas"
layer = "silver_layer"

location_cols = ["id", "latitude", "longitude", "neighbourhood", "neighborhood_overview",
                 "neighbourhood_cleansed", "neighbourhood_group_cleansed"]

listing_cols = ["id", "host_id", "listing_url", "name", "description",
                "picture_url", "property_type", "room_type", "accommodates", "bathrooms",
                # "bathrooms_text",
                "bedrooms", "beds", "amenities", "price",
                "has_availability", "availability_30", "availability_60", "availability_90", "availability_365",
                "instant_bookable", "license"]

host_cols = ["host_id", "host_url", "host_name", "host_since", "host_location",
            "host_about", "host_response_time", "host_response_rate", "host_acceptance_rate", "host_is_superhost",
            "host_thumbnail_url", "host_picture_url", "host_neighbourhood", "host_listings_count", "host_total_listings_count",
            "host_verifications", "host_has_profile_pic", "host_identity_verified"]

review_cols = ["id", "number_of_reviews", "number_of_reviews_ltm", "number_of_reviews_l30d", "first_review",
              "last_review", "review_scores_rating", "review_scores_accuracy", "review_scores_cleanliness", "review_scores_checkin",
              "review_scores_communication", "review_scores_location", "review_scores_value", "reviews_per_month"]

fact_cols = ["id", "scrape_id", "last_scraped", "calendar_last_scraped", "source",
            "calendar_updated", "minimum_nights", "maximum_nights", "minimum_minimum_nights", "maximum_minimum_nights",
            "minimum_maximum_nights", "maximum_maximum_nights", "minimum_nights_avg_ntm", "maximum_nights_avg_ntm", "calculated_host_listings_count",
            "calculated_host_listings_count_entire_homes", "calculated_host_listings_count_private_rooms", "calculated_host_listings_count_shared_rooms"]

# Utility functions for data transformation
def convert_special_text_into_numeric(text):
  """Converts special formatted text into numeric values, specifically for bathroom data."""
  if isinstance(text, str):
    if "half-bath" in text.lower():
      return 0.5
    else:
      try:
        return float(text.split()[0])
      except ValueError:
        return np.nan
  else:
    return text

def convert_boolean_into_numeric(col):
  """Converts boolean 't'/'f' strings into integers 1/0."""
  mapping = {"t": 1, "f": 0}
  return col.map(mapping)

def convert_list_string_into_string(list_str):
  """Cleans and converts a list formatted as a string into a clean, comma-separated string."""
  if not list_str:
    return ""
  list_str = list_str.strip("[]")
  elements = [element.replace("'", "") for element in list_str.split(", ")]
  return ", ".join(elements)

def data_processing(context, df):
  """Processes dataframe to clean and transform data."""
  context.log.info(f"Length of columns: {len(df.columns)}")

  # Processing specific columns
  df["id"] = pd.to_numeric(df["id"], errors="coerce").dropna().astype("int64")
  df["neighbourhood_cleansed"] = df["neighbourhood_cleansed"].astype(str)
  df["price"] = df["price"].astype("str").str.replace("$", "").str.replace(",", "")
  df["price"] = pd.to_numeric(df["price"], errors='coerce')

  # Boolean into numeric
  bool_cols = ["host_is_superhost", "host_has_profile_pic", "host_identity_verified", "has_availability", "instant_bookable"]
  for col in bool_cols:
    df[col] = convert_boolean_into_numeric(df[col])

  # String to float
  str_cols = ["minimum_nights", "minimum_maximum_nights", "maximum_maximum_nights", "availability_365"]
  for col in str_cols:
    df[col] = df[col].replace(",", "").astype(float)

  # List string to string
  df["host_verifications"] = df["host_verifications"].apply(convert_list_string_into_string)
  df["amenities"] = df["amenities"].apply(convert_list_string_into_string)

  # Fill NA with specific case
  df["bathrooms"] = df["bathrooms"].fillna(df["bathrooms_text"].apply(convert_special_text_into_numeric))

  # Drop unnecessary columns
  drop_cols = ["bathrooms_text", ]
  df.drop(columns=drop_cols, axis=1)

  # Imputation
  median_cols = ["host_response_rate", "host_acceptance_rate",
  ]
  most_freq_cols = ["host_is_superhost", 'host_listings_count', 'host_total_listings_count',
                    "host_verifications",
                    "host_has_profile_pic", "host_identity_verified",
                    "property_type", "room_type",
                    "accommodates", "bathrooms", "bedrooms", "beds",
                    "minimum_nights", "maximum_nights", "minimum_minimum_nights", "maximum_minimum_nights", "minimum_maximum_nights",
                    "maximum_maximum_nights", "minimum_nights_avg_ntm", "maximum_nights_avg_ntm",
                    "has_availability",
                    "availability_30", "availability_60", "availability_90", "availability_365",
                    "number_of_reviews", "number_of_reviews_ltm", "number_of_reviews_l30d",
                    "instant_bookable",
                    'calculated_host_listings_count', 'calculated_host_listings_count_entire_homes', 'calculated_host_listings_count_private_rooms', 'calculated_host_listings_count_shared_rooms'
  ]
  mean_cols = ["price",
                "review_scores_rating", "review_scores_accuracy", "review_scores_cleanliness", "review_scores_checkin",
                "review_scores_communication", "review_scores_location", "review_scores_value", "reviews_per_month"
  ]

  for col in median_cols:
    df[col] = df[col].astype("str").str.rstrip("%")
    df[col] = pd.to_numeric(df[col], errors='coerce')
    median_value = df[col].median()
    df[col] = df[col].fillna(median_value)

  for col in most_freq_cols:
    mode_val = df[col].mode()[0]
    df[col] = df[col].fillna(mode_val)

  for col in mean_cols:
    mean_val = df[col].mean()
    df[col] = df[col].fillna(mean_val)

  return df

@asset(
  io_manager_key="minio_io_manager",
  ins={name: AssetIn(key_prefix=["bronze"]) for name in return_dynamic_asset_names()},
  key_prefix=["silver"],
  group_name=layer,
  compute_kind=compute_kind,
)
def location_table(context, **dataframes) -> Output:
  df = pd.concat(dataframes.values())
  df = data_processing(context, df)
  location_df = df[location_cols].drop_duplicates().reset_index(drop=True)
  return Output(
    location_df,
    metadata={
      "table": "location_table",
      "records count": len(location_df),
      "columns count": len(location_df.columns)
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
  listing_df = df[listing_cols].drop_duplicates().reset_index(drop=True)
  return Output(
    listing_df,
    metadata={
      "table": "listing_table",
      "records count": len(listing_df),
      "columns count": len(listing_df.columns)
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
  host_df = df[host_cols].drop_duplicates().reset_index(drop=True)
  return Output(
    host_df,
    metadata={
      "table": "host_table",
      "records count": len(host_df),
      "columns count": len(host_df.columns)
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
  review_df = df[review_cols].drop_duplicates().reset_index(drop=True)
  return Output(
    review_df,
    metadata={
      "table": "review_table",
      "records count": len(review_df),
      "column count": len(review_df.columns)
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
  fact_df = df[fact_cols].drop_duplicates().reset_index(drop=True)
  return Output(
    fact_df,
    metadata={
      "table": "fact_table",
      "records count": len(fact_df),
      "columns count": len(fact_df.columns)
    }
  )
