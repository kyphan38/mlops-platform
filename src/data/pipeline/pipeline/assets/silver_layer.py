import pandas as pd
import numpy as np
from datetime import datetime
from dagster import asset, AssetIn, Output

from .bronze_layer import return_dynamic_asset_names
from ..utils.processing import host_response_time_processing, host_verifications_processing, property_type_processing, bathrooms_processing
from ..utils.imputation import missing_data_handling
from ..utils.checking import df_description

silver_data_dir = "./data/silver"
compute_kind = "Pandas"
layer = "silver_layer"

location_cols = ["id", "latitude", "longitude",
                 "neighbourhood", "neighborhood_overview", "neighbourhood_cleansed", "neighbourhood_group_cleansed",
                 "event_timestamp"]

listing_cols = ["id", "host_id", "listing_url", "name", "description",
                "picture_url", "property_type", "room_type", "accommodates", "bathrooms",
                # "bathrooms_text",
                "bedrooms", "beds", "amenities",
                "price",
                "has_availability",
                "availability_30", "availability_60", "availability_90", "availability_365",
                "instant_bookable", "license",
                "event_timestamp"]

host_cols = ["host_id", "host_url", "host_name", "host_since", "host_location",
            "host_about", "host_response_time", "host_response_rate", "host_acceptance_rate", "host_is_superhost",
            "host_thumbnail_url", "host_picture_url", "host_neighbourhood", "host_listings_count", "host_total_listings_count",
            "host_verifications", "host_has_profile_pic", "host_identity_verified",
            "event_timestamp"]

review_cols = ["id",
               "number_of_reviews", "number_of_reviews_ltm", "number_of_reviews_l30d", "first_review",
              "last_review",
              "review_scores_rating", "review_scores_accuracy", "review_scores_cleanliness", "review_scores_checkin",
              "review_scores_communication", "review_scores_location", "review_scores_value", "reviews_per_month",
              "event_timestamp"]

fact_cols = ["id", "scrape_id", "last_scraped", "calendar_last_scraped", "source",
            "calendar_updated",
            "minimum_nights", "maximum_nights", "minimum_minimum_nights", "maximum_minimum_nights", "minimum_maximum_nights", "maximum_maximum_nights", "minimum_nights_avg_ntm", "maximum_nights_avg_ntm",
            "calculated_host_listings_count", "calculated_host_listings_count_entire_homes", "calculated_host_listings_count_private_rooms", "calculated_host_listings_count_shared_rooms",
            "event_timestamp"]

categorical_cols = ["host_response_time", "host_is_superhost", "host_verifications",
                    "host_has_profile_pic", "host_identity_verified",
                    "property_type", "room_type",
                    "has_availability", "instant_bookable",]

numerical_cols = ["host_response_rate", "host_acceptance_rate",
                  "host_listings_count", "host_total_listings_count",
                  "accommodates", "bathrooms", "bedrooms", "beds",
                  "price",
                  "minimum_nights", "maximum_nights", "minimum_minimum_nights", "maximum_minimum_nights", "minimum_maximum_nights", "maximum_maximum_nights",
                  "minimum_nights_avg_ntm", "maximum_nights_avg_ntm",
                  "availability_30", "availability_60", "availability_90", "availability_365",
                  "number_of_reviews", "number_of_reviews_ltm", "number_of_reviews_l30d",
                  "review_scores_rating", "review_scores_accuracy", "review_scores_cleanliness", "review_scores_checkin",
                  "review_scores_communication", "review_scores_location", "review_scores_value", "reviews_per_month",]

def data_processing(context, df):
  # Drop some incorrect data points
  df["id"] = pd.to_numeric(df["id"], errors="coerce").dropna().astype("int64")

  # Add the event timestamp
  df["event_timestamp"] = datetime.now()

  # host_response_time
  df = host_response_time_processing(df, "host_response_time")

  # host_response_rate, host_response_time
  cols = ["host_response_rate", "host_acceptance_rate"]
  for col in cols:
    df[col] = df[col].replace(["None", "nan", "NaN", "", "null"], np.nan)
    df[col] = df[col].astype(str).str.rstrip("%")
    df[col] = pd.to_numeric(df[col], errors="coerce") # Use to_numeric instead of astype because it will replace non-numeric values with NaN

  # host_listings_count, host_total_listings_count | accommodates, bedrooms, beds | minimum_nights, minimum_maximum_nights | availability_30, availability_60, availability_90, availability_365 | number_of_reviews, number_of_reviews_ltm, number_of_reviews_l30d
  cols = ["host_listings_count", "host_total_listings_count",
          "accommodates", "bedrooms", "beds",
          "minimum_nights", "maximum_nights",
          "availability_30", "availability_60", "availability_90", "availability_365",
          "number_of_reviews", "number_of_reviews_ltm", "number_of_reviews_l30d"]
  for col in cols:
    df[col] = df[col].astype("float32")

  # host_verifications
  df = host_verifications_processing(df, "host_verifications")

  # property_type
  df["property_type"] = df["property_type"].apply(property_type_processing)

  # bathrooms
  df["bathrooms"] = df["bathrooms"].fillna(df["bathrooms_text"].apply(bathrooms_processing))
  df.drop(columns=["bathrooms_text"], inplace=True)

  # price
  df["price"] = df["price"].replace(["None", "nan", "NaN", "", "null"], np.nan)
  df["price"] = df["price"].astype(str).str.replace("$", "").str.replace(",", "")
  df["price"] = pd.to_numeric(df["price"], errors="coerce")

  # neighbour_hood cleansed
  df["neighbourhood_cleansed"] = df["neighbourhood_cleansed"].astype(str)

  return df

# Location table
@asset(
  name="location_table",
  key_prefix=["silver"],
  ins={name: AssetIn(key_prefix=["bronze"]) for name in return_dynamic_asset_names()},
  io_manager_key="minio_io_manager",
  compute_kind=compute_kind,
  group_name=layer,
)
def location_table(context, **dataframes) -> Output:
  df = pd.concat(dataframes.values())
  df = data_processing(context, df)
  df = missing_data_handling(context, df, numerical_cols, categorical_cols)
  df = df[location_cols].drop_duplicates(subset=["id"]).reset_index(drop=True)
  df_description(context, df)

  return Output(
    df,
    metadata={
      "table": "location_table",
      "records count": len(df),
      "columns count": len(df.columns)
    }
  )

# Listing table
@asset(
  name="listing_table",
  key_prefix=["silver"],
  ins={name: AssetIn(key_prefix=["bronze"]) for name in return_dynamic_asset_names()},
  deps=[location_table],
  io_manager_key="minio_io_manager",
  compute_kind=compute_kind,
  group_name=layer,
)
def listing_table(context, **dataframes) -> Output:
  df = pd.concat(dataframes.values())
  df = data_processing(context, df)
  df = missing_data_handling(context, df, numerical_cols, categorical_cols)
  df = df[listing_cols].drop_duplicates(subset=["id"]).reset_index(drop=True)
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
  key_prefix=["silver"],
  ins={name: AssetIn(key_prefix=["bronze"]) for name in return_dynamic_asset_names()},
  deps=[listing_table],
  io_manager_key="minio_io_manager",
  compute_kind=compute_kind,
  group_name=layer,
)
def host_table(context, **dataframes) -> Output:
  df = pd.concat(dataframes.values())
  df = data_processing(context, df)
  df = missing_data_handling(context, df, numerical_cols, categorical_cols)
  df = df[host_cols].drop_duplicates(subset=["host_id"]).reset_index(drop=True)
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
  key_prefix=["silver"],
  ins={name: AssetIn(key_prefix=["bronze"]) for name in return_dynamic_asset_names()},
  deps=[host_table],
  io_manager_key="minio_io_manager",
  compute_kind=compute_kind,
  group_name=layer,
)
def review_table(context, **dataframes) -> Output:
  df = pd.concat(dataframes.values())
  df = data_processing(context, df)
  df = missing_data_handling(context, df, numerical_cols, categorical_cols)
  df = df[review_cols].drop_duplicates(subset=["id"]).reset_index(drop=True)
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
  name="fact_table",
  key_prefix=["silver"],
  ins={name: AssetIn(key_prefix=["bronze"]) for name in return_dynamic_asset_names()},
  deps=[review_table],
  io_manager_key="minio_io_manager",
  compute_kind=compute_kind,
  group_name=layer,
)
def fact_table(context, **dataframes) -> Output:
  df = pd.concat(dataframes.values())
  df = data_processing(context, df)
  df = missing_data_handling(context, df, numerical_cols, categorical_cols)
  df = df[fact_cols].drop_duplicates(subset=["id"]).reset_index(drop=True)
  df_description(context, df)

  return Output(
    df,
    metadata={
      "table": "fact_table",
      "records count": len(df),
      "columns count": len(df.columns)
    }
  )
