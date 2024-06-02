import pandas as pd

def data_encoding(df):

  categorical_cols = ["host_response_time", "host_is_superhost", "host_verifications",
                    "host_has_profile_pic", "host_identity_verified",
                    "property_type", "room_type",
                    "has_availability", "instant_bookable",]

  df_encoded = pd.get_dummies(df, columns=categorical_cols)

  return df_encoded
