# from fastapi import FastAPI
# from pydantic import BaseModel
# import pandas as pd
# import numpy as np
# from sklearn.preprocessing import RobustScaler
# from utils.model.transforming import yeo_johnson_transforming
# from utils.model.imputation import missing_data_handling
# from feast import FeatureStore
# import mlflow
# import mlflow.sklearn
# import uvicorn

# class DataInput(BaseModel):
#   id: float
#   host_id: float
#   accommodates: float
#   bathrooms: float
#   bedrooms: float
#   beds: float
#   availability_30: float
#   availability_60: float
#   availability_90: float
#   availability_365: float
#   host_response_rate: float
#   host_acceptance_rate: float
#   host_listings_count: float
#   host_total_listings_count: float
#   number_of_reviews: float
#   number_of_reviews_ltm: float
#   number_of_reviews_l30d: float
#   review_scores_rating: float
#   review_scores_accuracy: float
#   review_scores_cleanliness: float
#   review_scores_checkin: float
#   review_scores_communication: float
#   review_scores_location: float
#   review_scores_value: float
#   reviews_per_month: float
#   minimum_nights: float
#   maximum_nights: float
#   minimum_minimum_nights: float
#   maximum_minimum_nights: float
#   minimum_maximum_nights: float
#   maximum_maximum_nights: float
#   minimum_nights_avg_ntm: float
#   maximum_nights_avg_ntm: float
  
# class ModelServing:
#   def __init__(self, model):
#     self.model = model

#   def data_transforming(self, df):
#     # Data dropping
#     df.drop(columns="id", "host_id", axis=1, inplace=True)
    
#     # Outliers handling
#     df = missing_data_handling(df)

#     # Data transforming
#     df = yeo_johnson_transforming(df)
    
#     # Data standardizing
#     scaler = RobustScaler()
#     df = scaler.fit_transform(df)
    
#     return df

#   def data_prediction(self, sample_data):
#     data = self.data_transforming(sample_data)
#     pred = self.model.predict(data)
#     return pred

# app = FastAPI()

# def load_best_model(run_id, model_name):
#     model_uri = f"runs:/{run_id}/{model_name}"
#     model = mlflow.sklearn.load_model(model_uri)
#     return model

# @app.post("/predict")
# async def predict(data_input: DataInput):
#   data_dict = data_input.dict()
#   df = pd.DataFrame(data_dict)
#   pred = model_serving.data_prediction(df)

#   return {
#     "prediction": pred.tolist()
#   }

# if __name__ == "__main__": 
#   best_model_run_id, best_model_name = "adc12572abe04f1eb83ab14a1fb0f111", "Decision_Tree_Regression"
#   model = load_best_model(best_model_run_id, best_model_name)
#   model_serving = ModelServing(model)
#   uvicorn.run(app, host="0.0.0.0", port=8000)

{
  "id": 2,
  "host_id": 2992450.0,
  "accommodates": 4.0,
  "bathrooms": 1.0,
  "bedrooms": 2.0,
  "beds": 2.2361068367009524,
  "availability_30": 0.0,
  "availability_60": 0.0,
  "availability_90": 0.0,
  "availability_365": 36.0,
  "host_response_rate": 100.0,
  "host_acceptance_rate": 100.0,
  "host_listings_count": 1.0,
  "host_total_listings_count": 5.0,
  "number_of_reviews": 9.0,
  "number_of_reviews_ltm": 0.0,
  "number_of_reviews_l30d": 0.0,
  "review_scores_rating": 4.51,
  "review_scores_accuracy": 4.879706019274778,
  "review_scores_cleanliness": 4.812461133714737,
  "review_scores_checkin": 4.82 ,
  "review_scores_communication": 4.944250346120556,
  "review_scores_location": 4.867251870622564,
  "review_scores_value": 4.790738114906661,
  "reviews_per_month": 0.08,
  "minimum_nights": 28.0,
  "maximum_nights": 1125.0,
  "minimum_minimum_nights": 28.0,
  "maximum_minimum_nights": 28.0,
  "minimum_maximum_nights": 1125.0,
  "maximum_maximum_nights": 1125.0,
  "minimum_nights_avg_ntm": 28.0,
  "maximum_nights_avg_ntm": 1125.0
}