from feast.infra.offline_stores.contrib.postgres_offline_store.postgres_source import PostgreSQLSource

listing_source = PostgreSQLSource(
  name="listing_table",
  table="listing_table",
  query="SELECT * FROM listing_table",
  timestamp_field="event_timestamp"
)

# host_source = PostgreSQLSource(
#   name="host_table",
#   table="host_table",
#   query="SELECT * FROM host_table",
#   timestamp_field="event_timestamp"
# )

# review_source = PostgreSQLSource(
#   name="review_table",
#   table="review_table",
#   query="SELECT *, event_timestamp as review_event_timestamp FROM review_table",
#   timestamp_field="review_event_timestamp"
# )

# fact_source = PostgreSQLSource(
#   name="fact_table",
#   table="fact_table",
#   query="SELECT *, event_timestamp as fact_event_timestamp FROM fact_table",
#   timestamp_field="fact_event_timestamp"
# )
