import numpy as np
import pandas as pd
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer

def convert_outliers_to_null(df):
  for col in df.select_dtypes(include=[np.number]).columns:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    outliers = (df[col] < lower_bound) | (df[col] > upper_bound)
    
    df.loc[outliers, col] = np.nan
            
  return df

def missing_data_handling(df):
  numerical_cols = ["host_response_rate", "host_acceptance_rate",
                  "host_listings_count", "host_total_listings_count",
                  "accommodates", "bathrooms", "bedrooms", "beds",
                  # "price",
                  "minimum_nights", "maximum_nights", "minimum_minimum_nights", "maximum_minimum_nights", "minimum_maximum_nights", "maximum_maximum_nights",
                  "minimum_nights_avg_ntm", "maximum_nights_avg_ntm",
                  "availability_30", "availability_60", "availability_90", "availability_365",
                  "number_of_reviews", "number_of_reviews_ltm", "number_of_reviews_l30d",
                  "review_scores_rating", "review_scores_accuracy", "review_scores_cleanliness", "review_scores_checkin",
                  "review_scores_communication", "review_scores_location", "review_scores_value", "reviews_per_month",]
  
  # Numerical columns
  df = convert_outliers_to_null(df)

  imputer = IterativeImputer(max_iter=5, verbose=2, random_state=0)
  df_cols = df[numerical_cols]
  df_cols_imputed = pd.DataFrame(imputer.fit_transform(df_cols), columns=df_cols.columns)
  df[numerical_cols] = df_cols_imputed

  return df