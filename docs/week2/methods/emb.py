import numpy as np
import pandas as pd
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Read the labeled data from CSV file
labled = pd.read_csv("NEWHELP_labeled_sequences.csv")

# Kidera factors dictionary (as per your input)
kidera_factors = {
    'A': [-1.56, -1.67, -0.97, -0.27, -0.93, -0.78, -0.2, -0.08, 0.21, -0.48],
    'C': [0.12, -0.89, 0.45, -1.05, -0.71, 2.41, 1.52, -0.69, 1.13, 1.1],
    'D': [0.58, -0.22, -1.58, 0.81, -0.92, 0.15, -1.52, 0.47, 0.76, 0.7],
    'E': [-1.45, 0.19, -1.61, 1.17, -1.31, 0.4, 0.04, 0.38, -0.35, -0.12],
    'F': [-0.21, 0.98, -0.36, -1.43, 0.22, -0.81, 0.67, 1.1, 1.71, -0.44],
    'G': [1.46, -1.96, -0.23, -0.16, 0.1, -0.11, 1.32, 2.36, -1.66, 0.46],
    'H': [-0.41, 0.52, -0.28, 0.28, 1.61, 1.01, -1.85, 0.47, 1.13, 1.63],
    'I': [-0.73, -0.16, 1.79, -0.77, -0.54, 0.03, -0.83, 0.51, 0.66, -1.78],
    'K': [-0.34, 0.82, -0.23, 1.7, 1.54, -1.62, 1.15, -0.08, -0.48, 0.6],
    'L': [-1.04, 0, -0.24, -1.1, -0.55, -2.05, 0.96, -0.76, 0.45, 0.93],
    'M': [-1.4, 0.18, -0.42, -0.73, 2, 1.52, 0.26, 1.23, -1.27, 0.27],
    'N': [1.14, -0.07, -0.12, 0.81, 0.18, 0.37, -0.09, -2.3, 1.1, -1.73],
    'P': [2.06, 0.24, -1.15, -0.75, 0.88, -0.45, 0.84, -0.71, 0.74, -0.28],
    'Q': [-0.47, 1.27, 0.07, 1.1, 1.1, 0.59, 0.92, -1.15, -0.03, -2.33],
    'R': [0.22, -0.7, 1.37, 1.87, -1.7, 0.46, 0.84, -0.39, 0.23, 0.93],
    'S': [0.81, 1.27, 0.16, 0.42, -0.21, -0.43, 0.92, -1.15, -0.97, -0.23],
    'T': [0.26, -1.08, 1.21, 0.63, -0.1, 0.21, 0.24, -1.15, -0.56, 0.19],
    'V': [-0.74, -0.7, 2.04, -0.4, 0.5, -0.81, -1.07, 0.06, -2.3, -0.6],
    'W': [0.3, -0.71, -0.72, -1.57, -1.16, 0.57, -0.48, -0.4, -0.05, 0.53],
    'Y': [1.38, 2.1, 0.8, -0.56, 0, -0.68, -0.31, 1.03, -0.6, 0.53]
}

default_kidera_vector = [0.0] * 10  # Default vector for unknown amino acids

def compute_kidera_embedding(sequence, kidera_factors, default_kidera_vector):

    #Converts a sequence of amino acids into an array of Kidera factor embeddings.

    return np.array([kidera_factors.get(aa, default_kidera_vector) for aa in sequence])

def process_sequences(sequences, max_length, kidera_dict, default_vector):

   # Process the list of sequences, encode them with Kidera factors, and pad them to a uniform length.

    kidera_matrices = [compute_kidera_embedding(seq, kidera_dict, default_vector) for seq in sequences]
    return pad_sequences(kidera_matrices, maxlen=max_length, padding='post', dtype='float32')

sequences = labled['sequence'].tolist()  # Convert the 'sequence' column to a list

# Process the sequences and pad them
max_length = 409  # 256 Maximum length dervided from the average
kidera_encoded_sequences = process_sequences(sequences, max_length, kidera_factors, default_kidera_vector)

#Display processed sequences
#print(kidera_encoded_sequences[:2])
#print(labled.head())

#Bin extraction: 
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

data = pd.read_csv('NEWHELP_labeled_sequences.csv')

bincode = labled['bincode'].tolist()

label_encoder = LabelEncoder()
bincode_encoded = label_encoder.fit_transform(bincode)

print(bincode_encoded[:5]) #test