import pandas as pd
from Bio import SeqIO
import csv

data = pd.read_csv("mapmanreferencebins.results.txt", sep="\t")

# dictionary to store all identifiers of each family
family_dict = {}

for index, row in data.iterrows():
    family = row['NAME'].strip("'")
    protein_id = row['IDENTIFIER'].strip("'").lower()
    if(protein_id): # works for rows that have an identifier
        if(family not in family_dict):
            family_dict[family] = []
        family_dict[family].append(protein_id)
        print("running")


print(sum(len(v) for v in family_dict.values()))

proteins = "protein.fa"
protein_dict = {}

for record in SeqIO.parse(proteins, "fasta"):
    uniprot_id = record.id.split("|")[-1].lower()
    sequence = str(record.seq)
    protein_dict[uniprot_id] = sequence

# group by families
grouped_dict = {}
for family, protein_ids in family_dict.items():
    sequences = [protein_dict[p] for p in protein_ids if p in protein_dict]
    if sequences:
        grouped_dict[family] = sequences
    else:
        grouped_dict[family] = []


result = "labeled_sequences.csv"
with open(result, "w") as newfile:
    newfile.write("family,sequence\n")
    for family, sequences in grouped_dict.items():
        for seq in sequences:
            newfile.write(f"{family}, {seq}\n")

print("done")
import csv

cleaned_rows = []

with open("labeled_sequences.csv", "r") as infile:
    reader = csv.reader(infile)
    for row in reader:
        if len(row) > 2:  # Too many columns
            # Merge columns beyond the first two
            family = row[0]
            sequence = ''.join(row[1:]).replace('"', '').replace("'", "")  # Merge and clean quotes
            cleaned_rows.append([family, sequence])
        elif len(row) == 2:  # Normal row
            cleaned_rows.append(row)
        else:
            print(f"Skipping malformed row: {row}")

# Save the cleaned data
with open("cleaned_labeled_sequences.csv", "w") as outfile:
    writer = csv.writer(outfile)
    writer.writerows(cleaned_rows)


"""eader = csv.reader(open("labeled_sequences.csv", "rU"), delimiter=",")
writer = csv.writer(open("fix_labeled_sequences.csv", 'w'), delimiter=";")
writer.writerows(reader)

print("changed")"""




