import numpy as np

def df_description(context, df):
  # Check for missing values
  missing_values_count = df.isnull().sum()
  vals = []

  context.log.info(f"Length of dataframe: {len(df)}\n")

  for col in df.columns:
    missing_count = missing_values_count[col]
    col_type = df[col].dtype
    vals.append(f"Column: {col}, Missing Values: {missing_count}, Type: {col_type}")

  vals = "\n".join(vals)
  context.log.info(vals)

  # Check for outliers using the IQR method directly in the loop
  total_outliers_count = 0

  for col in df.select_dtypes(include=[np.number]).columns:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    outliers_count = ((df[col] < lower_bound) | (df[col] > upper_bound)).sum()
    total_outliers_count += outliers_count
    context.log.info(f"Column: {col}, Outliers: {outliers_count}")

  total_missing_values = missing_values_count.sum()
  context.log.info(f"Total Missing Values: {total_missing_values}")
  context.log.info(f"Total Outliers: {total_outliers_count}")

  return total_missing_values >= 0 and total_outliers_count >= 0
