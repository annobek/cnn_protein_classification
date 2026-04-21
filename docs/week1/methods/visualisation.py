import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


# pairwise plot (not so understandable)

df = pd.read_csv("embedded_proteins.csv")

sns.pairplot(df)
plt.title("Pairwise plots of the protein features")
plt.show()


# Heatmap (further analysis needed)


kidera_features = df.iloc[:, 1:]

corr_matrix = kidera_features.corr()

plt.figure(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm")
plt.title("Correlation Heatmap of Kidera Features")
plt.show()

