
import sys
import pandas as pd
import numpy as np
import msprime


genome_table_file = sys.argv[1]
population_history_file = sys.argv[2]
n_ind = int(sys.argv[3])
n_wf_generations = int(sys.argv[4])
out_path = sys.argv[5]




genome_table = pd.read_csv(
    genome_table_file,
    delimiter = "\t"
)

genome_table.to_csv(out_path + "/genome_table.txt", sep = "\t", index = False)

history = pd.read_csv(population_history_file, sep = "\t")


demography = msprime.Demography()
demography.add_population(name = "pop", initial_size = history["Ne"][0])

for change_ix in range(1, len(history)):
  demography.add_population_parameters_change(
      time = history["generations_ago"][change_ix],
      population = "pop",
      initial_size = history["Ne"][change_ix]
  )


for chr_ix in range(len(genome_table)):
  rec_rate = genome_table.genetic_length[chr_ix]/100/genome_table.length[chr_ix]
  ts = msprime.sim_ancestry(
    samples = n_ind,
    recombination_rate = rec_rate,
    sequence_length = genome_table.length[chr_ix],
    demography = demography,
    model = [msprime.DiscreteTimeWrightFisher(duration = n_wf_generations),
    msprime.StandardCoalescent()]
  )
  ts_mutated = msprime.sim_mutations(
    ts,
    rate = 1e-8
  )
  geno = ts_mutated.genotype_matrix()
  multiallele_filter = np.any(geno == 2, axis = 1)
  geno_filtered = geno[~multiallele_filter]
  map = pd.DataFrame(ts_mutated.sites_position, columns = ["bp"])
  map["M"] = map["bp"] / genome_table.length[chr_ix] * genome_table.genetic_length[chr_ix]/100
  map_filtered = map[~multiallele_filter]
  map_filtered.to_csv(out_path + genome_table.chr[chr_ix] + "_pos.txt")
  np.save(
    out_path + genome_table.chr[chr_ix] + ".npy",
    geno_filtered.transpose()
  )
