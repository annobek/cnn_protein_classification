import numpy as np
import csv


amino_acids_ki_factor = {
    'A' : [89.09,115,31,-7.020,27.5,0.77,0.77,52.6,88.3,-12.04],
    'R' : [174.20,225,124,-10.131,105.0,3.72,2.38,109.1,181.2,39.23],
    'N' : [132.12,160, 56,-9.424,58.7, 1.98,1.45,75.7,125.1,4.25],
    'D' : [133.1,150,54.,-9.296,40.0,1.99,1.43,68.4,110.8,23.22],
    'C' : [121.15,135,55,-8.190,44.6,1.38,1.22,68.3,112.4,3.95],
    'Q' : [146.15,180,85,-10.044,80.7,2.58,1.75,89.7,148.7,2.16],
    'E' : [147.13,190,83,-10.467,62.0,2.63,1.77,84.7,140.5,16.81],
    'G' : [75.07,75,3,-5.456,0.0,0.00,0.58,36.3,60.0,-7.85],
    'H': [155.16, 195.0, 96.0, -12.15, 79.0, 2.76, 1.78, 91.9, 152.6, 6.28],
    'I': [131.17, 175.0, 111.0, -9.512, 93.5, 1.83, 1.56, 102.0, 168.5, -18.32],
    'L': [131.17, 170.0, 111.0, -10.52, 93.5, 2.08, 1.54, 102.0, 168.5, -17.79],
    'K': [146.19, 200.0, 119.0, -9.666, 100.0, 2.94, 2.08, 105.1, 175.6, 9.71],
    'M': [149.21, 185.0, 105.0, -10.424, 94.1, 2.34, 1.8, 97.7, 162.2, -8.86],
    'F': [165.19, 210.0, 132.0, -12.485, 115.5, 2.97, 1.9, 113.9, 189.0, -21.98],
    'P': [115.13, 145.0, 32.5, -8.652, 41.9, 1.42, 1.25, 73.6, 122.2, 5.82],
    'S': [105.09, 115.0, 32.0, -7.782, 29.3, 1.28, 1.08, 54.9, 88.7, -1.54],
    'T': [119.12, 140.0, 61.0, -8.764, 51.3, 1.43, 1.24, 71.2, 118.2, -4.15],
    'W': [204.24, 255.0, 170.0, -14.42, 145.5, 3.58, 2.21, 135.4, 227.0, -16.19],
    'Y': [181.19, 230.0, 136.0, -12.36, 117.3, 3.36, 2.13, 116.2, 193.0, -1.51],
    'V': [117.15, 155.0, 84.0, -8.778, 71.5, 1.49, 1.29, 85.1, 141.4, -16.22]
    
}

# Default vector for unknown amino acids
default_kidera_vector = np.zeros(10)

def compute_kidera_embedding(sequence):
    factors = [amino_acids_ki_factor.get(aa, default_kidera_vector) for aa in sequence]
    # Calculate the mean vector (embedding) for the sequence
    return np.mean(factors, axis=0) if factors else default_kidera_vector


#embedding process

input = "cleaned_labeled_sequences.csv"
output = "embedded_proteins.csv"

embeddings = []

with open("cleaned_labeled_sequences.csv", "r") as file:
    reader = csv.reader(file)
    next(reader)  # Skip header
    for family, sequence in reader:
        embedding = compute_kidera_embedding(sequence.strip())
        embeddings.append((family.strip(), embedding))

"""with open("labeled_sequences.csv", "r") as file:
  reader = csv.reader(file)
  sequence = [row[1] for row in reader]"""
  
  
feature_dict = ["Molecular weight", "Residue accessible surface area in tripeptide", "Volume",
                  "Short and medium range non-bonded energy per residue", "Side chain volume",
                  "Distance between C-alpha and centroid of side chain",
                  "Radius of gyration of side chain", "Residue volume_B", "Residue volume_GC", 
                  "Transfer free energy to lipophilic phase" ]
  
  # Save the embeddings to a new CSV file
with open("embedded_proteins.csv", "w") as outfile:
    writer = csv.writer(outfile)
    writer.writerow(["family"] + feature_dict)  # Header
    for family, embedding in embeddings:
        writer.writerow([family] + embedding.tolist())
        
        
        

#Feature mit eig namen ersetzen - DONE
#Visulalisieren  - teilweise done
#Trainierien:
#lineare oder logistische regression
#Irgendwas berechnen und diskutieren
#Labbook


