## Results
|                          file                            |     content
|----------------------------------------------------------|------------------
|[properties.all.csv](./properties.all.csv)|All the amino acids' properties from AAIndex
|[properties.188.csv](./properties.188.csv)|All the amino acids' properties used in Kidera Paper
|[properties_normalized.188.csv](./properties_normalized.188.csv)|Normalized variant of [properties.188.csv](./properties.188.csv)
|[properties_normalized.all.csv](./properties_normalized.all.csv)|Normalized variant of [properties.all.csv](./properties.all.csv)

### Reproduce

[properties.all.csv](./properties.all.csv):
```bash
# executed on 30.11.2024
# system: Ubuntu 24.04.1 LTS
cd ../methods
bash get_aa_properties.sh
```

[properties.188.csv](./properties.188.csv):
 - manually selected 188 properties from [properties.all.csv](./properties.all.csv) that are mentioned in Table 1 of<br>
   _Kidera, A., Konishi, Y., Oka, M. et al. Statistical analysis of the physical properties of the 20 naturally occurring amino acids. J Protein Chem 4, 23–55 (1985). https://doi.org/10.1007/BF01025492_
 - property 51: Average surrounding hydrophobicity (Ponnuswamy et al., 1980)
   - not found in AAIndex, only entry by Manavalan&Ponnuswamy, but this is already property 35
   - thus, NA values
 - property 115: Average relative fractional occurrence in E<sub>O</sub>(i) (Rackovsky&Scheraga, 1982)
   - as it is duplicate of property 73, we have taken E<sub>L</sub>(i), may've been a mistake in paper
 - property 139: Conformation parameter of a-helix (Finkelstein&Ptitsyn, 1976) (Pro:0.10)
   - not found in AAIndex, only one from 1977
   - thus, NA values
 - property 176: Average relative fractional occurrence in E<sub>L</sub>(i-1) (Rackovsky&Scheraga, 1982)
   - as it is duplicate of property 88, we have taken E<sub>0</sub>(i-1), may've been a mistake in paper

[properties_normalized.188.csv](./properties_normalized.188.csv) and [properties_normalized.all.csv](./properties_normalized.all.csv):
```bash
# executed on 02.12.2024
# system: Ubuntu 24.04.1 LTS
# python3: 3.12.3
# python3-pandas: 2.1.4
cd ../methods
python3 normalize_aa_properties.py ../results/properties.188.csv > ../results/properties_normalized.188.csv
python3 normalize_aa_properties.py ../results/properties.all.csv > ../results/properties_normalized.all.csv
```