# msprime to AlphaSimR scripts

This repository contains Python and R scripts to use a founder population simulated with `msprime` as the starting point for a simulation in `AlphaSimR`.

## Requirements

Python: `msprime`, `numpy`, `pandas`.

R: `AlphaSimR`, `readr`, `purrr`


## Contents

* `python/` directory: scripts for running `msprime` with a given population history and subsetting the output randomly.

* `R/` directory: scripts for importing founder haplotypes and map into `AlphaSimR`.

* `genomes/` directory: text files with physical and genetic length of chromosomes.

* `population_histories/`: text files with population histories.


## Use

Simulate founder population for 1000 cattle:

```
mkdir -p simulations/founders_full

python python/simulate_founders.py \
       genomes/cattle_genome_table.txt \
       population_histories/macleod2013.txt \
       1000 \
       200 \
       simulations/founders_full/
```

Sample 100 founders and 50,000 variants from that:

```
mkdir -p simulations/founders1

python python/sample_founders.py \
       genomes/cattle_genome_table.txt \
       simulations/founders_full/ \
       100 \
       50000 \
       simulations/founders1/
```

Finally, in an R session:

```
library(AlphaSimR)
source("R/import_msprime.R")
founders <- import_msprime("simulations/founders1")
```
