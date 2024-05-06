import pandas as pd
from dagster import asset, AssetIn, Output

from .bronze_layer import return_dynamic_asset_names

silver_data_dir = "./data/silver"
compute_kind = "Pandas"
layer = "silver_layer"

location_cols = ["id", "latitude", "longitude", "neighbourhood", "neighbourhood_cleansed",
                "neighbourhood_group_cleansed"]
                  #  "City", "State", "Country"]

listing_cols = ["id", "host_id", "listing_url", "name", "description",
                "picture_url", "property_type", "room_type", "accommodates", "bathrooms",
                "bathrooms_text", "bedrooms", "beds", "amenities", "price",
                "has_availability", "availability_30", "availability_60", "availability_90", "availability_365",
                "number_of_reviews", "instant_bookable", "license"]

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

@asset(
  io_manager_key="minio_io_manager",
  ins={name: AssetIn(key_prefix=["bronze"]) for name in return_dynamic_asset_names()},
  key_prefix=["silver"],
  group_name=layer,
  compute_kind=compute_kind,
)
def location_table(context, **dataframes) -> Output:
  df = pd.concat(dataframes.values())
  location_df = df[location_cols].drop_duplicates().reset_index(drop=True)
  return Output(
    location_df,
    metadata={
      "table": "location_table",
      "records count": len(location_df),
    }
  )

@asset(
  io_manager_key="minio_io_manager",
  ins={name: AssetIn(key_prefix=["bronze"]) for name in return_dynamic_asset_names()},
  key_prefix=["silver"],
  group_name=layer,
  compute_kind=compute_kind,
)
def listing_table(context, **dataframes) -> Output:
  df = pd.concat(dataframes.values())
  listing_df = df[listing_cols].drop_duplicates().reset_index(drop=True)
  return Output(
    listing_df,
    metadata={
      "table": "listing_table",
      "records count": len(listing_df),
    }
  )

@asset(
  io_manager_key="minio_io_manager",
  ins={name: AssetIn(key_prefix=["bronze"]) for name in return_dynamic_asset_names()},
  key_prefix=["silver"],
  group_name=layer,
  compute_kind=compute_kind,
)
def host_table(context, **dataframes) -> Output:
  df = pd.concat(dataframes.values())
  host_df = df[host_cols].drop_duplicates().reset_index(drop=True)
  return Output(
    host_df,
    metadata={
      "table": "host_table",
      "records count": len(host_df),
    }
  )

@asset(
  io_manager_key="minio_io_manager",
  ins={name: AssetIn(key_prefix=["bronze"]) for name in return_dynamic_asset_names()},
  key_prefix=["silver"],
  group_name=layer,
  compute_kind=compute_kind,
)
def review_table(context, **dataframes) -> Output:
  df = pd.concat(dataframes.values())
  review_df = df[review_cols].drop_duplicates().reset_index(drop=True)
  return Output(
    review_df,
    metadata={
      "table": "review_table",
      "records count": len(review_df),
    }
  )

@asset(
  io_manager_key="minio_io_manager",
  ins={name: AssetIn(key_prefix=["bronze"]) for name in return_dynamic_asset_names()},
  key_prefix=["silver"],
  group_name=layer,
  compute_kind=compute_kind,
)
def fact_table(context, **dataframes) -> Output:
  df = pd.concat(dataframes.values())
  fact_df = df[fact_cols].drop_duplicates().reset_index(drop=True)
  return Output(
    fact_df,
    metadata={
      "table": "fact_table",
      "records count": len(fact_df),
    }
  )
