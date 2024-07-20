from dagster import Definitions

from .assets.data_extraction import data_extraction
from .assets.data_validation import data_validation
from .assets.data_preparation import data_preparation
from .assets.model_training import model_training
from .assets.model_validation import model_validation
from .assets.model_exporting import model_exporting

defs = Definitions(
  assets=[data_extraction, data_validation, data_preparation] + [model_training, model_validation, model_exporting]
)
