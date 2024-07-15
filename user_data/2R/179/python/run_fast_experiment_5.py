"""
Simulation experiment
"""

import os
import pickle
import logging
import pandas as pd
import numpy as np
from scipy.optimize import least_squares
import gcubed
import gcubed.projections
from gcubed.projections.baseline_projections import BaselineProjections
from gcubed.runners.simple_runner import SimpleRunner
from gcubed.runners.simulation_runner import SimulationRunner
from gcubed.model_configuration import ModelConfiguration
from model_constants import (
    CONFIGURATION,
    CONFIGURATION_FILE,
    EXPERIMENT_RESULTS_FOLDER,
    EXPERIMENT_5 as EXPERIMENT,
)

# Determine where the results will be saved.
results_folder: str = EXPERIMENT_RESULTS_FOLDER(
    experiment_script_name=os.path.basename(__file__)
)

# Fit a polynomial of this order to the control variable projections.
# 0 implies a constant path for the control variable.
# 1 implies a linear path for the control variable.
# 2 implies a quadratic path for the control variable.
# 3 implies a cubic path for the control variable.
# 4 implies a quartic path for the control variable.
polynomial_order: int = 0

# Set the first control year
first_control_year: int = 2018
"""
The first year in which changes can be made to the controls.
"""

# Set the last control year
last_control_year: int = 2150
"""
The last year in which changes can be made to the controls.
"""

# Set the name of the target filename
controls_filename: str = "controls.csv"
"""
The name of the controls file.
"""

# Set the name of the target filename
targets_filename: str = "targets.csv"
"""
The name of the targets file.
"""

# ----------------------------------------------------------------------------
# Configuration ends here.
# ----------------------------------------------------------------------------

experiment_name: str = EXPERIMENT.split(os.path.sep)[0]
"""
The name of the experiment directory in the simulations directory.
"""

# Generate the list of control years used for polynomials in objective
# function evaluation.
control_years: list[int] = list(range(first_control_year, last_control_year + 1))
control_years_integers: np.ndarray = np.array(
    range(0, last_control_year - first_control_year + 1)
).reshape(1, last_control_year - first_control_year + 1)

# Generate the column labels of the years where control values can change.
control_year_labels: list[str] = [str(x) for x in control_years]

# Get the timestamp for the results
timestamp: str = gcubed.now()

# Set up targets and controls files
logging.info(
    f"Updating the values in the controls file, {controls_filename} from {first_control_year} onwards."
)
absolute_path_of_controls_file: str = os.path.abspath(
    os.path.join(
        CONFIGURATION.simulations_directory,
        experiment_name,
        controls_filename,
    )
)
assert os.path.exists(
    absolute_path_of_controls_file
), f"Could not find {controls_filename} in the {experiment_name} experiment."

absolute_path_of_targets_file: str = os.path.abspath(
    os.path.join(
        CONFIGURATION.simulations_directory,
        experiment_name,
        targets_filename,
    )
)
assert os.path.exists(
    absolute_path_of_targets_file
), f"Could not find {targets_filename} in the {experiment_name} experiment."

# Check that the experiment design file exists.
assert os.path.exists(
    os.path.abspath(
        os.path.join(
            CONFIGURATION.simulations_directory,
            experiment_name,
            "design.csv",
        )
    )
), f"Could not find the design file for the {experiment_name} experiment."

# Load the previously saved baseline projections, if they exist.
pickle_file: str = os.path.join(results_folder, "baseline_projections.pickle")
if os.path.exists(pickle_file):
    logging.info(
        f"Loading previously generated baseline projections from {pickle_file}"
    )
    baseline_projections: BaselineProjections = pickle.load(open(pickle_file, "rb"))
    logging.info(f"Loaded the baseline projections")

# Solve the model and regenerate the baseline projections if not already done.
if not (
    "baseline_projections" in globals()
    and isinstance(baseline_projections, BaselineProjections)
):
    # Generate the baseline projections.
    simple_runner: SimpleRunner = SimpleRunner(
        configuration_file=CONFIGURATION_FILE,
    )
    simple_runner.run()
    baseline_projections: BaselineProjections = simple_runner.baseline_projections
    with open(pickle_file, "wb") as file:
        pickle.dump(baseline_projections, file)
    logging.info(f"Generated the baseline projections after solving the model")

baseline_projections.charting_projections.to_csv(
    os.path.join(results_folder, f"baseline projections.csv")
)

# Load the targets CSV file.
targets = pd.read_csv(
    absolute_path_of_targets_file,
    header=0,
    index_col=0,
)

# Load the starting CSV controls file to get starting values for controls.
controls = pd.read_csv(
    absolute_path_of_controls_file,
    header=0,
    index_col=0,
).astype(float)

# Set up the starting vector for the least squares solver.
# The start_x vector contains the values of each cell in the DataFrame,
# obtained by stacking the rows one after the other and then
# flattening the resulting array.
# Thus the first set of elements are for the first control variable
# and those are followed by the values for the second control variable etc.
start_x: np.ndarray = np.zeros(
    shape=(len(controls.index), polynomial_order + 1)
).flatten()

iteration: int = 1

def objective_function(x: np.ndarray) -> np.ndarray:
    """

    ### Overview

    The objective function passed as an input to the least squares
    algorithm.

    The input `x` is converted to a set of values for the exogenous
    variables that are the control variables. The simulation is then
    run with these control variable values. The resulting projections are
    compared to the target projections and the differences are returned as a vector.

    The least squares algorithm drives these differences to zero by minimising
    a quadratic function of these differences.

    ### Arguments

    `x`: The vector of values being used to evaluate the objective function.

    ### Returns

    The return value, the vector of actual projections less target projections,
    evaluated for the vector of input control variables, x.
    """

    global iteration

    # Enable easy access of polynomial coefficients for each control variable.
    coefficients: np.ndarray = x.reshape(len(controls.index), polynomial_order + 1)

    control_values: np.ndarray = np.tile(
        coefficients[:, 0].reshape(len(controls.index), 1),
        (1, control_years_integers.shape[1]),
    )
    if polynomial_order > 0:
        for i in range(1, polynomial_order + 1):
            control_values: np.ndarray = control_values + (
                coefficients[:, i].reshape(len(controls.index), 1)
                * (control_years_integers**i)
            )

    # Save the candidate control values to the simulation layer file to run the simulation
    new_control_values: pd.DataFrame = pd.DataFrame(
        control_values,
        index=controls.index,
        columns=control_year_labels,
    ).astype(float)

    controls.loc[:, control_year_labels] = new_control_values.to_numpy()
    controls.to_csv(absolute_path_of_controls_file)

    # Set up the simulation runner.
    runner: SimulationRunner = SimulationRunner(
        baseline_projections=baseline_projections,
        experiment_design_file=os.path.join(experiment_name, "design.csv"),
    )

    # Run the simulation experiment.
    runner.run()

    # Access the final projections from the runner.
    trial_projections: pd.DataFrame = (
        runner.final_projections.publishable_projections.loc[
            targets.index, targets.columns
        ]
    )

    errors: pd.DataFrame = gcubed.projections.differences(
        original_projections=targets,
        new_projections=trial_projections,
    )
    logging.info(
        f"Iteration {iteration}:\n\nThe polynomial coefficients are:\n{coefficients}\nThe controls are:\n{controls.loc[:, control_year_labels]}\nThe differences from target are:\n{errors}\n\n")

    result: np.ndarray = errors.to_numpy().flatten()

    iteration += 1
    return result


# Run the optimisation and report results
solver_results = least_squares(fun=objective_function, x0=start_x, xtol=1e-2, ftol=1e-2)
logging.info(f"Solver results: {solver_results}")


# Set up the simulation runner to run with the final set of control values.
runner: SimulationRunner = SimulationRunner(
    baseline_projections=baseline_projections,
    experiment_design_file=EXPERIMENT,
)

# Run the simulation a last time using the optimised controls projections.
runner.run()

# Save the results
runner.final_projections.charting_projections.to_csv(
    os.path.join(results_folder, f"final projections.csv")
)

deviations: pd.DataFrame = gcubed.projections.deviations(
    new_projections=runner.final_projections,
    original_projections=runner.baseline_projections
)

deviations.to_csv(
    os.path.join(results_folder, "deviations.csv")
)