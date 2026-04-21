 # Protein classification using CNN model

 Team members:

- Shatu Ahmed (Matr.N. 2134985)
- Anna Beketova (Matr.N. 2176220)

## Overview

This project implements a machine learning pipeline for protein classification using a Convolutional Neural Network (CNN).

The workflow includes data preprocessing, feature engineering (sequence embedding using Kidera factors), model training, and evaluation. 
The model is trained to classify protein sequences into functional groups (Mapman bins).

The project demonstrates experience with deep learning, data processing, and working with structured biological datasets.

## Technical information

Following software was used for the project:

- Python:
    - Function: Programming language, used to carry out the specified tasks in this paper, including implementing the Embedding process and machine learning model 
    - Version: Python 3.11.7
    
- JupyterLab:
    - Function: [AI- server](ki.inf.th-bingen.de) provided by TH Bingen, where all scripts and program were carried out on due to the demanding RAM
    - Version: 3.6.7

- https://app.diagrams.net/
    - Function: Flowchart maker and Diagram software
    - Version: 26.0.16

Following Python libraries were used:

- numpy
- pandas
- tensorflow
- Bio
- csv
- sklearn
- torch
- torchmetrics
- matplotlib
- sys
- os


## Project navigation

- [material](material/) folder contains all data originating from third parties, such as the mapman table and reference proteins in the table.
- [methods](methods/) folder contains all scripts used for the project.
- [results](results/) folder contains all results data generated from the analysis of material and intermediate results.
    - [Experiment_plots](results/Experiment_plots) folder contains all experiment plots used in final reports.
- [docs](docs/) folder contains scientific reports, weekly materials such as weekly reports and weekly lab notebooks. Every week has its respective directory containing the neccessary documentations (Labbooks) and materials: 
    - [week1](docs/week1/)
    - [week2](docs/week2/)
    - [week3](docs/week3/)
    - [week4](docs/week4/)
    - [week5](docs/week5/)
    - [week6](docs/week6/)
    - [week7](docs/week7/)
    - [short_report](docs/short_report/) contains short one-page report about the best experiment.

## Folder details

### material

The protein sequences and their assignments to groups (Mapman Bins) of the same molecular function are in the files `Mapman_reference_DB_202310.tar.bz2` and `mapman.tar.bz`. The files were already extracted and placed in two folders: [old_dataset](material/old_dataset/) and [updated_dataset](material/updated_dataset/).

Extract data with `tar xjf <filename>` if needed. 

About the Mapman Bin Table:

- Bins are organized into trees.
- Only leaf nodes are assigned to actual proteins
- Very few protenis have more than one Bin
- Assignments were found by parsing for the last column (`TYPE`) set to `T` (True)
- BINCODE are identifiers that parse from the root of the Mapman Bin tree to the leaves. Each level is separated by points. The name of each level can be found at the respective BINCODE line.

About the datasets:

Originally used dataset is in [old_dataset](material/old_dataset/).

Content:
- `mapmanreferencebins.results.txt` the mapman table. 
- `protein.fa` - the reference proteins in the above table

Updated dataset is in the [updated_dataset](material/updated_dataset/) folder and has following features:

- Header has the form BINCODE, IDENTIFIER
- Bins 35.* and 50.* are removed
- The apostrophes are removed for simple parsing

Content:
- `mapman.tsv` - the updated mapman table
- `protein.fa`- updated reference proteins
- `README.md` - information about filtering the bincodes, so that only the one largest bin per root bin is kept, and information for reproducibility
- Python scripts needed for filtering and reproducibility


### methods

`get_aa_properties.sh` was provided, but wasn't actually used in the project.

`data_precrocessing.py` - performs preprocessing of the protein data: maps sequences to their corresponding bincodes.

`embedding.py` - performs embedding: sequences are encoded with Kidera factors and truncated to definded sequence length.

`labeling_training.py` - performs labeling and actual training of CNN models

`labeling_training_cross.py` - performs labeling and actual training with additional cross validation

### results

`properties.188.csv` and `properties.all.csv` are the results from running the `get_aa_properties.sh` script (see [methods](methods/) folder). The files weren't generated from the group, since they were already provided (see README.md in [results](results/) folder).

In the files `kidera_encoded_compressed.npz`, `training_output_1500_adam.txt` and `cross_validation_output_1500_adam.txt` sequences with the length of 1500 aminoacids are used as an output example. More plots are in [Experiment_plots](results/Experiment_plots/).


## Reproducibility steps

Ensure all Python libraries listed in **Technical information** above are installed.

The scripts can be executed with Linux Terminal. It is also recommended to perform embedding and training with strong GPU (for example on [TH Bingen AI Server](ki.inf.th-bingen.de)).

Results of the models with same parameters could differ slightly after each execution (~0.004 difference in Precision, Recall, F1-Score and MCC).

### 1. Dataset preparation

The `mapman.tsv` file needs to be filtered, in order to keep only the one largest bin per root bin (see `README.md` in [material/updated_dataset](material/updated_dataset/) folder)

Run following bash commands:

`python3 material/updated_dataset/filter_mapman.py material/updated_dataset/mapman.tsv > results/mapman_filtered.tsv`

and

`python3 material/updated_dataset/filter_prots.py results/mapman_filtered.tsv material/updated_dataset/protein.fa > results/protein_filtered.fa`

This will create two files in [results](results/) folder:

- `mapman_filtered.tsv` - will be used for labeling and embedding
- `protein_filtered.fa` - will be used for extracting the actual protein sequences for training

### 2. Data preprocessing

Run the script `data_preprocessing.py`, that is located in [methods](methods/) folder. The message `Preprocessing results saved.` will be shown, and two files will be saved in [results](results/) folder:

- `labeled_sequences_newdataset.csv` - intermediate result, protein sequences are assigned to bincodes. 
- `NEW_labeled_sequences.csv` - cleaned final result of preprocessing, falsely added columns are merged; the file will be used further.

### 3. Embedding

Run the script `embedding.py` that is located in [methods](methods/) folder. You might get some warnings about Tensorflow, but they shouldn't influence the output. The script execution could take some time.

After that the message `Embedding results saved` will be shown in the Terminal, and `kidera_encoded_compressed.npz` file will be created in [results](results/) folder. This is an intermediate result, where the 3D Array with protein sequences embedded with 10 Kidera factors and padded to a custom sequence length is saved to be used as an input for training.

When needed, modify the `max_length` parameter in the code (line 53) to perform padding with different sequence length.

### 4. Labeling and Training

*In this script no cross validation is implemented. See **step 5**, if you want to perform training with cross validation.*

Before running the script make sure that on the line 114 in `dummy_input = torch.rand(1, 10, z)` the value of z corresponds to the `max_length`, defined during the **Embedding** step.

Run the script `labeling_training.py` that is located in [methods](methods/). You might get some warnings about torch, but they shouldn't influence the output. You will also get the message `Training in progress...`. The script execution could take some time depending on the sequence length that was defined during embedding step (e.g. ~15 minutes for the length of 1500 aminoacids if executed on the TH Bingen AI Server) and hardware, where the project is executed.

After that the messages `Training output saved.` and `Training and validation loss graphs saved.` will be shown in the Terminal, and following files will be saved in [results](results/) folder:

- `training_validation_loss.png` - training and validation losses visualized
- `training_output.txt` - information about each epoch, training time and metrics values

Rename the files based on the performed experiment. 

If needed, modify the following in the script:

- Uncomment on lines 96, 99, 102, 105, 110, 128, 131, 134, 137 and 139 to add dropout layers.

- Adjust the function `optimizer = torch.optim.Adam(model.parameters(), lr=0.0001)` on line 151 for different optimizers, learning rates and to add weight decay.


### 5. (Optional) Training with cross validation

Before running the script make sure that on the line 60 in `dummy_input = torch.rand(1, 10, z)` the value of z corresponds to the `max_length`, defined during the **Embedding** step.

If you want to perform training with cross validation, run the script `labeling_training_cross.py` that is located in [methods](methods/) **instead of** `labeling_training.py`. You might get some warnings about torch, but they shouldn't influence the output. You will also get the message `Cross validation in progress...`. The script execution could take some time depending on the sequence length that was defined during embedding step (~1 hour for the length of 1500 aminoacids if executed in the TH Bingen AI Server) and hardware, where the project is executed.

After that the message `Cross validation output saved.` will be shown in the Terminal, and the file `cross_validation_output.txt` will be saved in [results](results/) folder. 

Rename the file based on the performed experiment. 

If needed, adjust the function `optimizer = torch.optim.Adam(model.parameters(), lr=0.0001)` in line 109 for different optimizers, learning rates and to add weight decay.
