"""
Just set the model up - good for generating diagnostics etc but not used for actual experiments.
"""

import os
import logging
from gcubed.model import Model
from gcubed.sym_data import SymData
from model_constants import CONFIGURATION, EXPERIMENT_RESULTS_FOLDER


# Determine where the results will be saved.
results_folder: str = EXPERIMENT_RESULTS_FOLDER(
    experiment_script_name=os.path.basename(__file__)
)

sym_data: SymData = SymData(configuration=CONFIGURATION)

model: Model = Model(configuration=CONFIGURATION)

logging.debug(
    f"Set up model version {model.configuration.version} build {model.configuration.build}"
)
