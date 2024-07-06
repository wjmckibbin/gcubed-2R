# Overview

This document describes model 2R build 178 which is a fork from 2R build 179.

Run the model using Python G-Cubed version 3.+.

## Changes from model 2R build 178

Migrates to a new way of representing the labor productivity growth assumptions, replacing the prodmat.csv file in the data directory with 3 files:

1. technology_advancement_rates.csv
2. technology_gaps.csv
3. technology_catchup_rates.csv

The derived data files are now:

1. labor_augmenting_technical_changes.csv produced from the above three files.
2. baseline_exogenous_projections.csv produced from the labor_augmenting_technical_changes.csv, the labor_force_growth_rates.csv file and the aeei.csv file.

Relaxes the assumption that the USA is the technology frontier region for all sectors, allowing the frontier region to differ across sectors and then all other regions can then catch up to that region.

Renamed the various files used to produce and work with the baseline exogenous variable adjustments.


