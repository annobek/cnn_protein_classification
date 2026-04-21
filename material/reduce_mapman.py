import pandas as pd
from sys import argv as args

mapman = pd.read_csv(args[1], sep="\t", quotechar="'")

# keep only rows with protein identifiers
mapman = mapman.loc[~mapman.IDENTIFIER.isna()]

# remove bins for unclassified ones
mapman = mapman.loc[~mapman.BINCODE.str.startswith("35.") & ~mapman.BINCODE.str.startswith("50.")]

# make identifiers uppercase
mapman.IDENTIFIER = mapman.IDENTIFIER.str.upper()

print(mapman[["BINCODE", "IDENTIFIER"]].to_csv(index=False, sep="\t"), end="")
