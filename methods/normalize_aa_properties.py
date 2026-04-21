import pandas as pd
from sys import argv as args

properties = pd.read_csv(args[1])

for i in range(len(properties.index)):
    # read amino acid values, skip despription column
    prop_vector = properties.iloc[i, 1:]

    # center the data -> mean is 0
    prop_vector -= prop_vector.mean()

    # scale the data -> std deviation is 1
    prop_vector /= prop_vector.std()

    # update table
    properties.iloc[i, 1:] = prop_vector

print(properties.to_csv(index=False), end="")
