def df_description(context, df):
  missing_values_count = df.isnull().sum()
  vals = []

  for col in df.columns:
    missing_count = missing_values_count[col]
    col_type = df[col].dtype
    vals.append(f"Column: {col}, Missing Values: {missing_count}, Type: {col_type}")

  vals = "\n".join(vals)
  context.log.info(vals)
