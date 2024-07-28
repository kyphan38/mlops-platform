import mlflow

# def create_mlflow_experiment(experiment_name, artifact_location):
#   try:
#     experiment_id= mlflow.create_experiment(
#       name=experiment_name,
#       artifact_location=artifact_location
#     )
#   except mlflow.exceptions.MlflowException:
#     context.log.info(f"Experiment {experiment_name} already exists.")
#     experiment_id = mlflow.get_experiment_by_name(experiment_name).experiment_id

#   mlflow.set_experiment(experiment_name=experiment_name)

#   return experiment_id

# import mlflow
# from mlflow.exceptions import MlflowException

# def create_mlflow_experiment(context, experiment_name, artifact_location):
#     try:
#         experiment_id = mlflow.create_experiment(
#             name=experiment_name,
#             artifact_location=artifact_location
#         )
#     except MlflowException as e:
#         if "RESOURCE_ALREADY_EXISTS" in str(e) or "BAD_REQUEST" in str(e):
#             experiment = mlflow.get_experiment_by_name(experiment_name)
#             if experiment is not None:
#                 experiment_id = experiment.experiment_id
#             else:
#                 context.log.error(f"Experiment '{experiment_name}' exists but couldn't retrieve its ID.")
#                 raise e
#         else:
#             context.log.error(f"Failed to create or get experiment: {e}")
#             raise e
#     return experiment_id
