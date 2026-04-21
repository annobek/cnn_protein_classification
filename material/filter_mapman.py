import pandas as pd
from sys import argv as args

mapman = pd.read_csv(args[1], sep="\t", index_col="BINCODE")
bin_sizes = mapman.index.value_counts()

root_bins = bin_sizes.index.str.split(".").str[0]
max_sized_bins_per_root = bin_sizes.groupby(root_bins).idxmax()
mapman = mapman.loc[max_sized_bins_per_root]

print(mapman.to_csv(sep="\t"))
