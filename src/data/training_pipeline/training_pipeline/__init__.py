from dagster import job, Definitions

from .assets.data_extraction import data_extraction
from .assets.data_validation import data_validation
from .assets.data_preparation import data_preparation

defs = Definitions(
  assets=[data_extraction] + [data_validation] + [data_preparation],
)
