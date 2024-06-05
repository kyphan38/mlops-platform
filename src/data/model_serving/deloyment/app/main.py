import logging
from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import os
from sklearn.preprocessing import RobustScaler
from utils.transforming import yeo_johnson_transforming
from utils.imputation import missing_data_handling
from feast import FeatureStore
import mlflow
import mlflow.sklearn
import uvicorn
from prometheus_fastapi_instrumentator import Instrumentator

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DataInput(BaseModel):
  id: float
  host_id: float
  accommodates: float
  bathrooms: float
  bedrooms: float
  beds: float
  availability_30: float
  availability_60: float
  availability_90: float
  availability_365: float
  host_response_rate: float
  host_acceptance_rate: float
  host_listings_count: float
  host_total_listings_count: float
  number_of_reviews: float
  number_of_reviews_ltm: float
  number_of_reviews_l30d: float
  review_scores_rating: float
  review_scores_accuracy: float
  review_scores_cleanliness: float
  review_scores_checkin: float
  review_scores_communication: float
  review_scores_location: float
  review_scores_value: float
  reviews_per_month: float
  minimum_nights: float
  maximum_nights: float
  minimum_minimum_nights: float
  maximum_minimum_nights: float
  minimum_maximum_nights: float
  maximum_maximum_nights: float
  minimum_nights_avg_ntm: float
  maximum_nights_avg_ntm: float

class ModelServing:
  def __init__(self, model):
    self.model = model

  def data_transforming(self, df):
    # Data dropping
    df.drop(columns=["id", "host_id"], axis=1, inplace=True)
    
    # Outliers handling
    df = missing_data_handling(df)

    # Data transforming
    df = yeo_johnson_transforming(df)
    
    # Data standardizing
    scaler = RobustScaler()
    df = scaler.fit_transform(df)
    
    return df

  def data_prediction(self, sample_data):
    data = self.data_transforming(sample_data)
    pred = self.model.predict(data)
    return pred

app = FastAPI()

def load_best_model(run_id, model_name):
  mlflow_tracking_uri = os.getenv('MLFLOW_TRACKING_URI')
  mlflow.set_tracking_uri(mlflow_tracking_uri)
  model_uri = f"runs:/{run_id}/{model_name}"
  model = mlflow.sklearn.load_model(model_uri)

  return model

best_model_run_id, best_model_name = "6f5ea1d794804da681cc85c0ff02c9dc", "Decision_Tree_Regression"
model = load_best_model(best_model_run_id, best_model_name)
model_serving = ModelServing(model)

# Instrumentation
instrumentator = Instrumentator().instrument(app).expose(app, endpoint="/metrics")

@app.post("/predict")
async def predict(data_input: DataInput):
  data_dict = data_input.dict()
  df = pd.DataFrame([data_dict])
  pred = model_serving.data_prediction(df)

  logger.info(f"Received data: {data_dict}")
  logger.info(f"Prediction result: {pred.tolist()}")

  return {
    "prediction result": pred.tolist()
  }