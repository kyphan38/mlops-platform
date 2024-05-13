import pandas as pd
import os

def merge_csv_files(input_path, output_path):
  os.makedirs(output_path, exist_ok=True)
  merged_file_path = os.path.join(output_path, "merged_data.csv")

  dfs = []

  for file_name in os.listdir(input_path):
    if file_name.endswith(".csv"):
      file_path = os.path.join(input_path, file_name)
      parts = file_name.replace(".csv", "").split("_")[1:]  # Skip the date part
      city = parts[0].replace("-", " ")
      state = parts[1].replace("-", " ")
      country = parts[2].replace("-", " ")

      df = pd.read_csv(file_path)
      df['City'] = city
      df['State'] = state
      df['Country'] = country

      dfs.append(df)

  merged_df = pd.concat(dfs, ignore_index=True)
  merged_df.to_csv(merged_file_path, index=False)


if __name__ == "__main__":
  input_path = "./data/raw"
  output_path = "./data/merged"

  merge_csv_files(input_path, output_path)
