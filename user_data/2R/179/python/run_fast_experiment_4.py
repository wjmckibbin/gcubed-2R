"""
Simulation experiment
"""

import logging
import os
import pickle
import pandas as pd
import numpy as np
import gcubed
import gcubed.projections
from gcubed.model import Model
from gcubed.model_configuration import ModelConfiguration
from gcubed.projections.projections import Projections
from gcubed.linearisation.solved_model import SolvedModel
from gcubed.projections.baseline_projections import BaselineProjections
from gcubed.runners.simulation_runner import SimulationRunner
from model_constants import (
    CONFIGURATION,
    EXPERIMENT_RESULTS_FOLDER,
    EXPERIMENT_4_A as EXPERIMENT_A,
    EXPERIMENT_4_B as EXPERIMENT_B,
)

# Determine where the results will be saved.
results_folder: str = EXPERIMENT_RESULTS_FOLDER(
    experiment_script_name=os.path.basename(__file__)
)

# Load the previously saved baseline projections, if they exist.
baseline_projections_pickle_file: str = os.path.join(
    results_folder, "baseline_projections.pickle"
)
if os.path.exists(baseline_projections_pickle_file):
    logging.info(
        f"Loading previously generated baseline projections from {baseline_projections_pickle_file}"
    )
    with open(baseline_projections_pickle_file, "rb") as file:
        baseline_projections: BaselineProjections = pickle.load(file)

# Solve the model and regenerate the baseline if not already done.
if not (
    "baseline_projections" in globals()
    and isinstance(baseline_projections, BaselineProjections)
):
    # Load or create the solved model first
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
        logging.info(f"Saved the solved model for later reuse.")

    baseline_projections: BaselineProjections = BaselineProjections(
        solved_model=solved_model
    )
    with open(baseline_projections_pickle_file, "wb") as file:
        pickle.dump(baseline_projections, file)
    logging.info(f"Saved the baseline projections for later reuse.")

baseline_projections.charting_projections.to_csv(
    os.path.join(
        results_folder,
        f"1 {baseline_projections.name}.csv",
    )
)

# Run simulation experiment A that builds on the baseline projections.
runner: SimulationRunner = SimulationRunner(
    baseline_projections=baseline_projections,
    experiment_design_file=EXPERIMENT_A,
)
runner.run()

# Save the first experiment's levels projections to a CSV file
simulation_A_final_projections: Projections = runner.final_projections
simulation_A_final_projections.charting_projections.to_csv(
    os.path.join(
        results_folder,
        f"2A {simulation_A_final_projections.name}.csv",
    )
)

# Run simulation experiment B that builds on the baseline projections.
runner: SimulationRunner = SimulationRunner(
    baseline_projections=baseline_projections,
    experiment_design_file=EXPERIMENT_B,
)
runner.run()

# Save the first experiment's levels projections to a CSV file
simulation_B_final_projections: Projections = runner.final_projections
simulation_B_final_projections.charting_projections.to_csv(
    os.path.join(
        results_folder,
        f"2B {simulation_B_final_projections.name}.csv",
    )
)

deviations_A: pd.DataFrame = gcubed.projections.deviations(
    new_projections=simulation_A_final_projections,
    original_projections=baseline_projections,
)
deviations_A.to_csv(
    os.path.join(
        results_folder,
        f"2A - 1 deviations of {simulation_A_final_projections.name} from {baseline_projections.name}.csv",
    )
)

deviations_B: pd.DataFrame = gcubed.projections.deviations(
    new_projections=simulation_B_final_projections,
    original_projections=baseline_projections,
)
deviations_B.to_csv(
    os.path.join(
        results_folder,
        f"2B - 1 deviations of {simulation_B_final_projections.name} from {baseline_projections.name}.csv",
    )
)

# Save the first experiment's deviation from baseline projections to a CSV file
deviations_A_from_B: pd.DataFrame = gcubed.projections.deviations(
    new_projections=simulation_A_final_projections,
    original_projections=simulation_B_final_projections,
)
deviations_A_from_B.to_csv(
    os.path.join(
        results_folder,
        f"2A - 2B deviations of {simulation_A_final_projections.name} from {simulation_B_final_projections.name}.csv",
    )
)
