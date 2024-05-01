import os
import requests
import gzip
import shutil
from bs4 import BeautifulSoup
from datetime import datetime
from dagster import asset, AssetIn, AssetOut

def download_and_extract(city, state, country, date, url, path):
  os.makedirs(path, exist_ok=True)
  date_format = datetime.strptime(date, "%d %B, %Y").strftime("%d%m%y")
  name_format = f"{date_format}_{city}_{state}_{country}.csv"
  output_path = os.path.join(path, name_format)

  if not os.path.exists(output_path):
    with requests.Session() as session:
      response = session.get(url)
      tmp_path = os.path.join(path, url.split("/")[-1])

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

@asset(
  name="crawl_data",
  description="Crawl data from official website of Airbnb",
  io_manager_key="minio_io_manager",
  key_prefix=["bronze"],
  group_name="bronze_layer"
)
def crawl_data():
  url = "http://insideairbnb.com/get-the-data"
  response = requests.get(url)
  html = response.text
  soup = BeautifulSoup(html, "html.parser")
  country_tp = ("United States", )

  for h3 in soup.find_all("h3"):
    text = h3.get_text().strip()
    if text.endswith(country_tp):
      if text.count(",") == 2:
        text_split = [x.strip() for x in text.split(",")]

        city = text_split[0].replace(" ", "-")
        state = text_split[1].replace(" ", "-")
        country = text_split[2].replace(" ", "-")

        date = h3.find_next_sibling("h4").get_text()
        date = date.split("(")[0].strip()

        link_table = h3.find_next_sibling("table")
        if link_table:
          links = link_table.find_all("a")
          for link in links:
            if "listings.csv.gz" in link["href"]:
              url = link["href"]
              download_and_extract(city, state, country, date, url, "./data/raw")
