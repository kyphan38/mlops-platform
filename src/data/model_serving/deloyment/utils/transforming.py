import numpy as np
from sklearn.preprocessing import PowerTransformer

def yeo_johnson_transforming(df):
  pt = PowerTransformer(method='yeo-johnson')
  
  for col in df.select_dtypes(include=[np.number]).columns:
      if col != "price": 
          df[col] = pt.fit_transform(df[[col]])

  return df