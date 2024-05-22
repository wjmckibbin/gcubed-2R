"""
Run the 'run_fast_baseline.py' script to solve the model and create baseline projections that can be used by other experiments.

Then run this script to create a results directory for each experiment Python script (identified by the `run` prefix in the file name)
and to create a symbolic link to all pickle files produced when the run_fast_baseline.py script has completed running successfully.

This is ensure that the experiments do not need to resolve the model or recreate the baseline projections, saving a lot of time.
"""

import logging
import os
from model_constants import (
    CONFIGURATION,
    ROOT_RESULTS_FOLDER,
    PYTHON_FOLDER,
)

BASELINE_GENERATION_SCRIPT: str = "run_fast_baseline.py"
full_path_to_baseline_generation_script: str = os.path.join(
    PYTHON_FOLDER, BASELINE_GENERATION_SCRIPT
)

assert os.path.exists(
    full_path_to_baseline_generation_script
), f"Cannot find the {full_path_to_baseline_generation_script} script."

baseline_results_folder: str = os.path.join(
    ROOT_RESULTS_FOLDER,
    CONFIGURATION.version,
    CONFIGURATION.build,
    f"{os.path.splitext(BASELINE_GENERATION_SCRIPT)[0]}",
)

# Get the list of Python scripts in the python folder that start with `run`.
experiment_scripts: list[str] = [
    file
    for file in os.listdir(PYTHON_FOLDER)
    if file.endswith(".py") and file.startswith("run")
]

assert os.path.exists(
    baseline_results_folder
), f"Cannot find the {baseline_results_folder} folder. Run the {full_path_to_baseline_generation_script} script first."

# Get the list of pickle files
pickle_files: list[str] = [
    file for file in os.listdir(baseline_results_folder) if file.endswith(".pickle")
]

for experiment_script in experiment_scripts:
    experiment_results_folder: str = os.path.join(
        ROOT_RESULTS_FOLDER,
        CONFIGURATION.version,
        CONFIGURATION.build,
        f"{os.path.splitext(experiment_script)[0]}",
    )
    if experiment_results_folder == baseline_results_folder:
        continue
    if not os.path.exists(experiment_results_folder):
        os.makedirs(experiment_results_folder)
    for pickle_file in pickle_files:
        os.symlink(
            os.path.join(baseline_results_folder, pickle_file),
            os.path.join(experiment_results_folder, pickle_file),
        )
