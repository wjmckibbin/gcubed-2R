# Simulation experiments

Several simulation experiments are provided as examples.

The Python scripts to run the experiments are in the `python` folder.

To run a script, open it in your VS Code devcontainer and click on the run arrow in the top right corner of the editor.

## Preliminaries

Before running the experiments:

1. Solve the model and create the baseline projections by running 

```bash
run_fast_baseline.py
```

2. Share the solved model and baseline projections with the experiments (so that they do not have to be reproduced for each experiment that is run) by running:

```bash
share_baseline_projections_with_experiments.py
```

## A temporary increase in the USA inflation target

The USA inflation target is increased by 1 percentage points (to 3.5%) for 3 years.

The experiment script is `run_fast_experiment_1.py`.

## A temporary increase in the USA inflation target

The USA inflation target is increased by 1 percentage points (to 3.5%) permanently.

The experiment script is `run_fast_experiment_2.py`.

## Unexpected reversal of permanent increase to inflation target in the USA.

The increase is in 2019 and it is unexpectedly reversed in 2026.

The experiment script is `run_fast_experiment_3.py`.

## Investment tax policy credit comparison

The experiment compares an anticipated investment tax credit policy to an unanticipated investment tax credit policy.

The experiment script is `run_fast_experiment_4.py`.

It uses two simulation layers that differ in terms of their event year.

It uses two design files, one for each simulation layer.

The Python script calculates the deviations due to the anticipation effect.

