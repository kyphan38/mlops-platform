# from dagster import Definitions

# from .jobs.feast_apply import hello_world_job

# defs = Definitions(
#   jobs=[hello_world_job],
# )

from dagster import Definitions
from .jobs.feast_apply import feast_apply_job

defs = Definitions(
    jobs=[feast_apply_job],
)
