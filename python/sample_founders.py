
import sys
import pandas as pd
import numpy as np
import random


genome_table_file = sys.argv[1]
founder_base_path = sys.argv[2]
n_ind = int(sys.argv[3])
n_seg_sites = int(sys.argv[4])
out_path = sys.argv[5]

genome_table = pd.read_csv(
    genome_table_file,
    delimiter = "\t"
)


genome_table["seg_sites"] = round(n_seg_sites * genome_table["length"] / sum(genome_table["length"]))

genome_table.to_csv(out_path + "/genome_table.txt", sep = "\t", index = False)

for chr_ix in range(len(genome_table)):
  ## read matrix and map
  haplo = np.load(founder_base_path + "/" + genome_table["chr"][chr_ix] + ".npy")
  map = pd.read_csv(founder_base_path + "/" + genome_table["chr"][chr_ix] + "_pos.txt", index_col = 0)
  ## randomly sample
  to_take = genome_table["seg_sites"][chr_ix].astype(int)
  pick = sorted(random.sample(range(0, len(map)), to_take))
  haplo_pick = haplo[:, pick]
  map_pick = map.iloc[pick, :]
  ## write matrix and map
  map_pick.to_csv(out_path + genome_table.chr[chr_ix] + "_pos.txt")
  np.savetxt(
    out_path + genome_table.chr[chr_ix] + ".txt",
    haplo_pick,
    fmt = "%1d"
  )
