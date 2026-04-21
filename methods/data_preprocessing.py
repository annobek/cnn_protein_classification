import pandas as pd
from Bio import SeqIO
import csv
import os

# Paths to the used files
mapman_path = os.path.join("..", "results", "mapman_filtered.tsv")
protein_path = os.path.join("..", "results", "protein_filtered.fa")
labeled_sequences_path = os.path.join("..", "results", "labeled_sequences_newdataset.csv")
cleaned_sequences_path = os.path.join("..", "results", "NEW_labeled_sequences.csv")


# Read mapman data
data = pd.read_csv(mapman_path, sep="\t")

# Process mapman file
bincode_dict = {} # dictionary to store all identifiers of each family

for index, row in data.iterrows():
    bincode = row['BINCODE'].strip("'")
    protein_id = row['IDENTIFIER'].strip("'").lower()
    if(protein_id):
        if(bincode not in bincode_dict):
            bincode_dict[bincode] = []
        bincode_dict[bincode].append(protein_id)


# Open and process protein fasta file
protein_dict = {}

for record in SeqIO.parse(protein_path, "fasta"):
    uniprot_id = record.id.split("|")[-1].lower()
    sequence = str(record.seq)
    protein_dict[uniprot_id] = sequence

grouped_dict = {}
for bincode, protein_ids in bincode_dict.items():
    sequences = [protein_dict[p] for p in protein_ids if p in protein_dict]
    if sequences:
        grouped_dict[bincode] = sequences
    else:
        grouped_dict[bincode] = []

# Assign proteins to bincodes
with open(labeled_sequences_path, "w") as newfile:
    newfile.write("bincode,sequence\n")
    for bincode, sequences in grouped_dict.items():
        for seq in sequences:
            newfile.write(f"{bincode}, {seq}\n")



# Clean the results
cleaned_rows = []

with open(labeled_sequences_path, "r") as infile:
    reader = csv.reader(infile)
    for row in reader:
        if len(row) > 2:
            bincode = row[0]
            sequence = ''.join(row[1:]).replace('"', '').replace("'", "") # Merge falsely added columns and clean quotes
            cleaned_rows.append([bincode, sequence])
        elif len(row) == 2:
            cleaned_rows.append(row)
        else:
            print(f"Skipping malformed row: {row}")


with open(cleaned_sequences_path, "w") as outfile:
    writer = csv.writer(outfile)
    writer.writerows(cleaned_rows)

print("Preprocessing results saved.")