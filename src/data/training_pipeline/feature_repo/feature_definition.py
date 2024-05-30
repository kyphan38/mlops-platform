from feast.types import Int64, Float64, String
from feast import Field, FeatureView
from datetime import timedelta

from entities import entity_id, entity_host_id
from data_sources import listing_source, host_source, review_source, fact_source

# Define the feature view
listing_fv = FeatureView(
  name="listing_feature_view",
  description="Feature view for listing table",
  entities=[entity_id],
  ttl=timedelta(days=36500),
  schema=[
    Field(name="host_id", dtype=Int64),
    Field(name="property_type", dtype=String),
    Field(name="room_type", dtype=String),
    Field(name="accommodates", dtype=Float64),
    Field(name="bathrooms", dtype=Float64),
    Field(name="bedrooms", dtype=Float64),
    Field(name="beds", dtype=Float64),
    Field(name="price", dtype=Float64),
    Field(name="has_availability", dtype=String),
    Field(name="availability_30", dtype=Float64),
    Field(name="availability_60", dtype=Float64),
    Field(name="availability_90", dtype=Float64),
    Field(name="availability_365", dtype=Float64),
    Field(name="instant_bookable", dtype=String),
  ],
  online=True,
  source=listing_source,
  tags={}
)

host_fv = FeatureView(
  name="host_feature_view",
  description="Feature view for host table",
  entities=[entity_host_id],
  ttl=timedelta(days=36500),
  schema=[
    Field(name="host_response_time", dtype=String),
    Field(name="host_response_rate", dtype=Float64),
    Field(name="host_acceptance_rate", dtype=Float64),
    Field(name="host_is_superhost", dtype=String),
    Field(name="host_listings_count", dtype=Float64),
    Field(name="host_total_listings_count", dtype=Float64),
    Field(name="host_verifications", dtype=String),
    Field(name="host_has_profile_pic", dtype=String),
    Field(name="host_identity_verified", dtype=String),
  ],
  online=True,
  source=host_source,
  tags={}
)

review_fv = FeatureView(
  name="review_feature_view",
  description="Feature view for review table",
  entities=[entity_id],
  ttl=timedelta(days=36500),
  schema=[
    Field(name="number_of_reviews", dtype=Int64),
    Field(name="number_of_reviews_ltm", dtype=Float64),
    Field(name="number_of_reviews_l30d", dtype=Float64),
    Field(name="review_scores_rating", dtype=Float64),
    Field(name="review_scores_accuracy", dtype=Float64),
    Field(name="review_scores_cleanliness", dtype=Float64),
    Field(name="review_scores_checkin", dtype=Float64),
    Field(name="review_scores_communication", dtype=Float64),
    Field(name="review_scores_location", dtype=Float64),
    Field(name="review_scores_value", dtype=Float64),
    Field(name="reviews_per_month", dtype=Float64),
  ],
  online=True,
  source=review_source,
  tags={}
)

fact_fv = FeatureView(
  name="fact_feature_view",
  description="Feature view for fact table",
  entities=[entity_id],
  ttl=timedelta(days=36500),
  schema=[
    Field(name="minimum_nights", dtype=Float64),
    Field(name="maximum_nights", dtype=Float64),
    Field(name="minimum_minimum_nights", dtype=Float64),
    Field(name="maximum_minimum_nights", dtype=Float64),
    Field(name="minimum_maximum_nights", dtype=Float64),
    Field(name="maximum_maximum_nights", dtype=Float64),
    Field(name="minimum_nights_avg_ntm", dtype=Float64),
    Field(name="maximum_nights_avg_ntm", dtype=Float64),
  ],
  online=True,
  source=fact_source,
  tags={}
)
