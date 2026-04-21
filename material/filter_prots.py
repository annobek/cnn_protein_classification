from tools import Fasta
from tqdm import tqdm
from sys import argv as args
import pandas as pd

mapman = pd.read_csv(args[1], sep="\t", index_col="IDENTIFIER").squeeze()
mapman = mapman[~mapman.str.startswith("35.") & ~mapman.str.startswith("50.")]

fasta_content = {}

for file in args[2:]:
    for p in Fasta(file):
        fasta_content[p[0]] = str(p)

for prot in tqdm(mapman.index.unique()):
    print(fasta_content[prot], end="")
