import pandas as pd

def missing_value(df):
  median_cols = ["host_response_rate", "host_acceptance_rate",
                 ]

  most_freq_cols = ["host_is_superhost", "host_listings_count", "host_total_listings_count",
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
                    "calculated_host_listings_count", "calculated_host_listings_count_entire_homes", "calculated_host_listings_count_private_rooms", "calculated_host_listings_count_shared_rooms"
                    ]

  mean_cols = ["price",
                "review_scores_rating", "review_scores_accuracy", "review_scores_cleanliness", "review_scores_checkin",
                "review_scores_communication", "review_scores_location", "review_scores_value", "reviews_per_month"
                ]

  for col in median_cols:
    df[col] = df[col].astype("str").str.rstrip("%")
    df[col] = pd.to_numeric(df[col], errors="coerce")
    median_value = df[col].median()
    df[col] = df[col].fillna(median_value)

  for col in most_freq_cols:
    mode_val = df[col].mode()[0]
    df[col] = df[col].fillna(mode_val)

  for col in mean_cols:
    mean_val = df[col].mean()
    df[col] = df[col].fillna(mean_val)

  return df
