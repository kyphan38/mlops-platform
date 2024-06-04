import requests
import json

# Define the URL of the FastAPI endpoint
url = "http://jupyter_notebook:8000/predict"

# Define the sample data input
data_input = {
    "id": 2.0,
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
    "review_scores_rating": None,
    "review_scores_accuracy": 4.879706019274778,
    "review_scores_cleanliness": 4.812461133714737,
    "review_scores_checkin": None,
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

# Send POST request to the FastAPI endpoint
response = requests.post(url, json=data_input)

# Print the response from the FastAPI server
print("Response Status Code:", response.status_code)
print("Response JSON:", response.json())
