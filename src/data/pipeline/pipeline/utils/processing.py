import numpy as np
import pandas as pd

def host_response_time_processing(df, col):
  df[col] = df[col].replace(np.nan, "unknown")
  return df

def host_verifications_processing(df, col):
  df[col] = df[col].str.replace(r"[\'\[\]]", "", regex=True)
  return df

def property_type_processing(val):
  if "Entire" in val:
      return "entire Place"
  elif "Private" in val:
      return "private Room"
  elif "Shared" in val:
      return "shared Room"
  else:
      return "unique Stay"

def bathrooms_processing(txt):
  if isinstance(txt, str):
    if "half-bath" in txt.lower():
      return 0.5
    else:
      try:
        return float(txt.split()[0])
      except ValueError:
        return np.nan
  else:
    return txt
