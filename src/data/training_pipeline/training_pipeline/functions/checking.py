def df_description(df):
  """
  Counts and prints the number of missing values in each column of the given DataFrame along with their data types.

  Parameters:
  df (pandas.DataFrame): The DataFrame to count and print missing values in.
  """
  missing_values_count = df.isnull().sum()
  for column in df.columns:
    missing_count = missing_values_count[column]
    col_type = df[column].dtype
    print(f'Column: {column}, Missing Values: {missing_count}, Type: {col_type}')
