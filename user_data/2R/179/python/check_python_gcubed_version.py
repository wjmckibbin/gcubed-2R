"""
Run the 'run_fast_baseline.py' script to solve the model and create baseline projections that can be used by other experiments.

Then run this script to create a results directory for each experiment Python script (identified by the `run` prefix in the file name)
and to create a symbolic link to all pickle files produced when the run_fast_baseline.py script has completed running successfully.

This is ensure that the experiments do not need to resolve the model or recreate the baseline projections, saving a lot of time.
"""

import gcubed


constants: gcubed.constants.Constants = gcubed.constants.Constants()
print(f"You are running G-Cubed version {constants.VERSION}")
