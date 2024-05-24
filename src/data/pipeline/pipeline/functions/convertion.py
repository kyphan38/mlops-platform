import numpy as np

def special_text_into_numeric(text):
  """Converts special formatted text into numeric values, specifically for bathroom data."""
  if isinstance(text, str):
    if "half-bath" in text.lower():
      return 0.5
    else:
      try:
        return float(text.split()[0])
      except ValueError:
        return np.nan
  else:
    return text

def boolean_into_numeric(col):
  """Converts boolean 't'/'f' strings into integers 1/0."""
  mapping = {"t": 1, "f": 0}
  return col.map(mapping)

def list_string_into_string(list_str):
  """Cleans and converts a list formatted as a string into a clean, comma-separated string."""
  if not list_str:
    return ""
  list_str = list_str.strip("[]")
  elements = [element.replace("'", "") for element in list_str.split(", ")]
  return ", ".join(elements)
