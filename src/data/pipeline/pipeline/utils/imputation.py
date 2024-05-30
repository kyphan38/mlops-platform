from sklearn.impute import SimpleImputer

def median_imputation(df, cols):
  for col in cols:
    median_val = df[col].median()
    df[col].fillna(median_val, inplace=True)

def mode_imputation(df, cols):
  for col in cols:
    mode_val = df[col].mode()[0]
    df[col].fillna(mode_val, inplace=True)
