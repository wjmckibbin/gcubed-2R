"""
Run the baseline but only resolve the model when needed.
"""

from math import exp
import os
import pickle
import logging
import pandas as pd
import numpy as np
import gcubed
from gcubed.model import Model
from gcubed.projections.baseline_projections import BaselineProjections
from gcubed.linearisation.solved_model import SolvedModel
from gcubed.model_configuration import ModelConfiguration
from model_constants import CONFIGURATION, EXPERIMENT_RESULTS_FOLDER

# Determine where the results will be saved.
results_folder: str = EXPERIMENT_RESULTS_FOLDER(
    experiment_script_name=os.path.basename(__file__)
)

# Check to see if a solved model has been pickled in the results folder.
solved_model_pickle_file: str = os.path.join(results_folder, "solved_model.pickle")
if os.path.exists(solved_model_pickle_file):
    logging.info(f"Loading previously solved model from {solved_model_pickle_file}")
    with open(solved_model_pickle_file, "rb") as file:
        solved_model: SolvedModel = pickle.load(file)

if not ("solved_model" in globals() and isinstance(solved_model, SolvedModel)):
    model: Model = Model(configuration=CONFIGURATION)
    solved_model: SolvedModel = SolvedModel(model=model)
    with open(solved_model_pickle_file, "wb") as file:
        pickle.dump(solved_model, file)
    logging.info(f"Pickled the solved model into the results folder for later reuse.")

# Generate the baseline projections
baseline_projections: BaselineProjections = BaselineProjections(
    solved_model=solved_model
)
baseline_projections_pickle_file: str = os.path.join(
    results_folder, "baseline_projections.pickle"
)
with open(baseline_projections_pickle_file, "wb") as file:
    pickle.dump(baseline_projections, file)

# Save the baseline projections to a CSV file to support graphical analysis.
baseline_projections.charting_projections.to_csv(
    os.path.join(
        results_folder,
        f"baseline projections.csv",
    )
)
