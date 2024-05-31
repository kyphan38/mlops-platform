import mlflow
import mlflow.sklearn
from sklearn.linear_model import LinearRegression
import numpy as np

# Set MLflow tracking URI to your MLflow server
mlflow.set_tracking_uri("http://mlflow:5000")

# Create a new experiment or use an existing one
experiment_name = "test_experiment5"
experiment = mlflow.get_experiment_by_name(experiment_name)
if experiment is None:
    experiment_id = mlflow.create_experiment(name=experiment_name, artifact_location="s3://artifacts")
else:
    experiment_id = experiment.experiment_id

# Create a simple Linear Regression model
model = LinearRegression()

# Generate some data
X = np.array([[1, 1], [1, 2], [2, 2], [2, 3]])
y = np.dot(X, np.array([1, 2])) + 3

# Train the model
model.fit(X, y)

# Start an MLflow run
with mlflow.start_run(run_name="test_run", experiment_id=experiment_id) as run:
    # Log the model
    mlflow.sklearn.log_model(model, "model")
    print("run_id: {}".format(run.info.run_id))
    print("experiment_id: {}".format(run.info.experiment_id))
    print("status: {}".format(run.info.status))
    print("start_time: {}".format(run.info.start_time))
    print("end_time: {}".format(run.info.end_time))
    print("lifecycle_stage: {}".format(run.info.lifecycle_stage))

print("Model logged successfully.")
