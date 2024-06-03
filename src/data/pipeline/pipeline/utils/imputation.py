import numpy as np
import pandas as pd
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer

def mode_imputation(df, cols):
  for col in cols:
    mode_val = df[col].mode()[0]
    df[col].fillna(mode_val, inplace=True)

def convert_outliers_to_null(context, df):
  for col in df.select_dtypes(include=[np.number]).columns:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    outliers = (df[col] < lower_bound) | (df[col] > upper_bound)
    
    df.loc[outliers, col] = np.nan
            
  return df

def missing_data_handling(context, df, numerical_cols, categorical_cols):
  # Numerical columns
  df = convert_outliers_to_null(context, df)

  imputer = IterativeImputer(max_iter=5, verbose=2, random_state=0)
  df_cols = df[numerical_cols]
  df_cols_imputed = pd.DataFrame(imputer.fit_transform(df_cols), columns=df_cols.columns)
  df[numerical_cols] = df_cols_imputed

  # Categorical columns
  mode_imputation(df, categorical_cols)

  return df