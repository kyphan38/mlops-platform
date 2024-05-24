import numpy as np

def log_transform(df):
  outlier_counts = {}
  for column in df.select_dtypes(include=[np.number]).columns:  # Select only numeric columns
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]
    outlier_counts[column] = len(outliers)

    if outlier_counts[column] > 0:  # Check if there are outliers in the column
      # Ensure that all values are positive
      min_value = df[column].min()
      if min_value <= 0:
          df[column] = df[column] + (-min_value + 1)

      # Apply log10 transformation
      df[column] = np.log10(df[column])

  return df
