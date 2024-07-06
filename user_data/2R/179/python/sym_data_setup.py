"""
Just set the sym data object up - good for generating diagnostics etc but not used for actual experiments.
"""

import os
from gcubed.sym_data import SymData
from model_constants import CONFIGURATION, EXPERIMENT_RESULTS_FOLDER


# Determine where the results will be saved.
results_folder: str = EXPERIMENT_RESULTS_FOLDER(
    experiment_script_name=os.path.basename(__file__)
)

sym_data: SymData = SymData(configuration=CONFIGURATION)

sym_data.variable_summary.to_csv(
    os.path.join(
        CONFIGURATION.diagnostics_directory, "sym_data_variable_summary_template.csv"
    )
)
