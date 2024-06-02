from dagster import Definitions
from .jobs.feast_apply import feast_apply_job

defs = Definitions(
    jobs=[feast_apply_job],
)
