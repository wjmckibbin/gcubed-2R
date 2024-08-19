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


## Midterm essay experiments

Before running these scripts, make sure you have done the preliminaries, described above.

Also be sure to use the fiscal closure module where the deficit is determined endogenously while spending is exogenous. Check the `sym/linear/ggg-configuration.sym` file to ensure that the relevant line is uncommented (does not start with `//`):

```sym
#include linear/gggopt-fiscal-closure-deficit-endogenous-spending-exogenous.sym
```

1. [USA government spending shock 1](experiment_Fiscal_USA_1/README.md)

2. [USA government spending shock 2](experiment_Fiscal_USA_2/README.md)

3. [Global government spending shock 1](experiment_Fiscal_Global_1/README.md)
## Example experiments

Each of the following example experiments can be run using the python script with the matching experiment number. Thus, for experiment 1, run:

```bash
run_fast_experiment_1.py
```

1. [A permanent increase in the USA inflation target](experiment_1/README.md)

2. [A temporary increase in the USA inflation target](experiment_2/README.md)

3. [Unexpected reversal of permanent increase to inflation target in the USA](experiment_3/README.md)

4. [Anticipation effect for an investment tax credit](experiment_4/README.md)

5. [Find potential output growth consistent with achieving target inflation](experiment_5/README.md)
