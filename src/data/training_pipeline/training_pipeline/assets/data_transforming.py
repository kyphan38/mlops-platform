from dagster import asset, AssetIn

@asset(ins={"df": AssetIn("ingest_data")})
def encoding_applying(df):
  df.drop('property_type', axis=1, inplace=True)
  df.drop('room_type', axis=1, inplace=True)
  df.drop('host_verifications', axis=1, inplace=True)
  df.drop('amenities', axis=1, inplace=True)

  return df
