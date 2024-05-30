import os
import requests
import gzip
import shutil
from datetime import datetime

def html_processing(soup, country_tp, data_dir):
  for h3 in soup.find_all("h3"):
    text = h3.get_text().strip()                                      # Output: Albany, New York, United States
    if text.endswith(country_tp):
      if text.count(",") == 2:
        text_split = [x.strip() for x in text.split(",")]

        city = text_split[0].replace(" ", "-")
        state = text_split[1].replace(" ", "-")
        country = text_split[2].replace(" ", "-")

        date = h3.find_next_sibling("h4").get_text()                  # Output: 10 March, 2024 (Explore)
        date = date.split("(")[0].strip()                             # Output: 10 March, 2024

        link_table = h3.find_next_sibling("table")
        if link_table:
          links = link_table.find_all("a")
          for link in links:
            if "listings.csv.gz" in link["href"]:
              url = link["href"]                                      # Output: https://data.insideairbnb.com/united-states/ny/albany/2024-03-10/data/listings.csv.gz
              data_downloading(city, state, country, date, url, data_dir)

def data_downloading(city, state, country, date, url, data_dir):
  os.makedirs(data_dir, exist_ok=True)

  date_format = datetime.strptime(date, "%d %B, %Y").strftime("%d%m%y")
  name_format = f"{city}_{state}_{country}_{date_format}.csv"
  output_path = os.path.join(data_dir, name_format)

  if not os.path.exists(output_path):
    with requests.Session() as session:                                # Open a request session TCP
      response = session.get(url)
      tmp_path = os.path.join(data_dir, url.split("/")[-1])            # Output: ./data/raw/listings.csv.gz

      if tmp_path.endswith(".gz"):
        with open(tmp_path, "wb") as file:
          file.write(response.content)
        with gzip.open(tmp_path, "rb") as file_in, open(output_path, "wb") as file_out:
          shutil.copyfileobj(file_in, file_out)
        os.remove(tmp_path)
      else:
        with open(tmp_path, "wb") as file:
          file.write(response.content)
        os.rename(tmp_path, output_path)
  else:
    print(f"File {name_format} already exists. Skipping download.")
