def df_description(context, df):
  missing_values_count = df.isnull().sum()
  vals = []

  for col in df.columns:
    missing_count = missing_values_count[col]
    col_type = df[col].dtype
    vals.append(f"Column: {col}, Missing Values: {missing_count}, Type: {col_type}")

  vals = "\n".join(vals)
  context.log.info(vals)

import pandas as pd
import numpy as np

def count_outliers(series):
  Q1 = series.quantile(0.25)
  Q3 = series.quantile(0.75)
  IQR = Q3 - Q1
  outliers = series[((series < (Q1 - 1.5 * IQR)) | (series > (Q3 + 1.5 * IQR)))]
  return outliers.count()

def collect_column_summary(df, col):
  data_type = df[col].dtype
  missing_values = df[col].isna().sum()
  outliers = count_outliers(df[col]) if pd.api.types.is_numeric_dtype(df[col]) else "N/A"
  return f"- Column '{col}' has data type '{data_type}', {outliers} outliers, and {missing_values} missing values"

def collect_all_columns_info(df, context, all_cols):
  summary = []
  for col in all_cols:
    summary.append(collect_column_summary(df, col))
    
  summary = "\n".join(summary)
  context.log.info(summary)
