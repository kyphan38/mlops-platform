import mlflow

def create_mlflow_experiment(experiment_name, artifact_location):
  try:
    experiment_id= mlflow.create_experiment(
      name=experiment_name,
      artifact_location=artifact_location
    )
  except mlflow.exceptions.MlflowException:
    print(f"Experiment {experiment_name} already exists.")
    experiment_id = mlflow.get_experiment_by_name(experiment_name).experiment_id

  mlflow.set_experiment(experiment_name=experiment_name)

  return experiment_id
