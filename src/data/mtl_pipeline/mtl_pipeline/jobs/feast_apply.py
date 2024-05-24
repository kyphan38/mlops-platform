import os
import subprocess
from dagster import job, op, Output

command = "feast apply; feast materialize-incremental $(date +%Y-%m-%d)"

@op
def feast_apply(context):
  cwd = os.getcwd()
  context.log.info(f"CWD: {cwd}")
  os.chdir("./feature_repo")

  result = subprocess.run(command, capture_output=True, text=True, shell=True)

  context.log.info(f"Command stdout: {result.stdout}")
  context.log.info(f"Command stderr: {result.stderr}")

@job
def feast_apply_job():
  feast_apply()
