import pandas as pd
from dagster import asset, AssetIn, Output

gold_data_dir = "./data/gold"
compute_kind = "Pandas"
layer = "gold_layer"

# location_cols = ["id", "latitude", "longitude", "neighbourhood", "neighbourhood_cleansed",
#                 "neighbourhood_group_cleansed"]

# @asset(
#   io_manager_key="minio_io_manager",
#   ins={"location_table": AssetIn(key_prefix=["silver"])},
#   key_prefix=["gold"],
#   group_name=layer,
#   compute_kind=compute_kind,
# )
# def rental_dataset(context,
#                    location_table: pd.DataFrame,
#                    ) -> Output:

#   df = location_table[location_cols]

#   return Output(
#     df,
#     metadata={
#       "table": "location_table",
#       "records count": len(df),
#       "columns count": len(df.columns)
#     }
#   )

listing_cols = ['id', 'host_id', 'property_type', 'room_type',
                'accommodates', 'bathrooms',
                # 'bathrooms_text',
                'bedrooms', 'beds', 'amenities', 'price', 'has_availability',
                'availability_30', 'availability_60', 'availability_90', 'availability_365',
                'instant_bookable',
                'event_timestamp'
                ]

host_cols = ['host_id', 'host_response_rate', 'host_acceptance_rate', 'host_is_superhost',
             'host_listings_count', 'host_total_listings_count', 'host_verifications',
             'host_has_profile_pic', 'host_identity_verified',
             'event_timestamp'
             ]

review_cols = ['id', 'number_of_reviews', 'number_of_reviews_ltm', 'number_of_reviews_l30d',
               'review_scores_rating', 'review_scores_accuracy', 'review_scores_cleanliness', 'review_scores_checkin',
               'review_scores_communication', 'review_scores_location', 'review_scores_value', 'reviews_per_month',
               'event_timestamp'
               ]

fact_cols = ['id', 'minimum_nights', 'maximum_nights', 'minimum_minimum_nights',
             'maximum_minimum_nights', 'minimum_maximum_nights', 'maximum_maximum_nights',
             'minimum_nights_avg_ntm', 'maximum_nights_avg_ntm',
             'calculated_host_listings_count', 'calculated_host_listings_count_entire_homes',
             'calculated_host_listings_count_private_rooms', 'calculated_host_listings_count_shared_rooms',
             'event_timestamp'
             ]

@asset(
  io_manager_key="minio_io_manager",
  ins={"listing_table": AssetIn(key_prefix=["silver"])},
  key_prefix=["gold"],
  group_name=layer,
  compute_kind=compute_kind,
)
def listing_table(context,
                   listing_table: pd.DataFrame,
                   ) -> Output:

  df = listing_table[listing_cols]

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
  ins={"host_table": AssetIn(key_prefix=["silver"])},
  key_prefix=["gold"],
  group_name=layer,
  compute_kind=compute_kind,
)
def host_table(context,
                   host_table: pd.DataFrame,
                   ) -> Output:

  df = host_table[host_cols]

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
  ins={"review_table": AssetIn(key_prefix=["silver"])},
  key_prefix=["gold"],
  group_name=layer,
  compute_kind=compute_kind,
)
def review_table(context,
                   review_table: pd.DataFrame,
                   ) -> Output:

  df = review_table[review_cols]

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
  ins={"fact_table": AssetIn(key_prefix=["silver"])},
  key_prefix=["gold"],
  group_name=layer,
  compute_kind=compute_kind,
)
def fact_table(context,
                   fact_table: pd.DataFrame,
                   ) -> Output:

  df = fact_table[fact_cols]

  return Output(
    df,
    metadata={
      "table": "location_table",
      "records count": len(df),
      "columns count": len(df.columns)
    }
  )
