import numpy as np

def outliers_handling(df):
  outlier_counts = {}
  for col in df.select_dtypes(include=[np.number]).columns:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
    outlier_counts[col] = len(outliers)

    if outlier_counts[col] > 0:
      min_value = df[col].min()
      if min_value <= 0:
        df[col] = df[col] + (-min_value + 1)

      # Apply log10 transformation
      df[col] = np.log10(df[col])

  return df
