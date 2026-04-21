import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset
from torchmetrics import Precision, Recall, F1Score, MatthewsCorrCoef
from sklearn.model_selection import KFold
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys 
from sklearn.preprocessing import MultiLabelBinarizer
import os

# Paths to the used files
cleaned_sequences_path = os.path.join("..", "results", "NEW_labeled_sequences.csv")
kidera_encoded_path = os.path.join("..", "results", "kidera_encoded_compressed.npz")
cross_validation_path = os.path.join("..", "results", "cross_validation_output.txt")

# Read the file with protein sequences
data = pd.read_csv(cleaned_sequences_path)

# Labeling step

# Convert 'bincode' into lists of labels
data['bincode'] = data['bincode'].str.split(', ')
mlb = MultiLabelBinarizer()
bincode_encoded = mlb.fit_transform(data['bincode'])  # Multi-hot encoding

# Load embedded data
loaded_data = np.load(kidera_encoded_path)
kidera_encoded_sequences = loaded_data['arr_0']

# Ensure reproducibility
torch.manual_seed(42)
np.random.seed(42)

# Dataset Preparation
kidera_encoded_sequences_tensor = torch.tensor(kidera_encoded_sequences, dtype=torch.float32)
labels_tensor = torch.tensor(bincode_encoded, dtype=torch.float32)

# Permute to [num_sequences, num_features, sequence_length]
kidera_encoded_sequences_tensor = kidera_encoded_sequences_tensor.permute(0, 2, 1)

# CNN Model defined
class ConvolutionalNetwork(nn.Module):
    def __init__(self, num_classes):
        super(ConvolutionalNetwork, self).__init__()
        self.conv1 = nn.Conv1d(in_channels=10, out_channels=32, kernel_size=7, stride=2)
        self.pool1 = nn.MaxPool1d(kernel_size=2, stride=2)
        self.conv2 = nn.Conv1d(in_channels=32, out_channels=64, kernel_size=5, stride=2)
        self.pool2 = nn.MaxPool1d(kernel_size=2, stride=2)
        self.conv3 = nn.Conv1d(in_channels=64, out_channels=128, kernel_size=3, stride=2)
        self.pool3 = nn.MaxPool1d(kernel_size=2, stride=2)
        self.conv4 = nn.Conv1d(in_channels=128, out_channels=256, kernel_size=3, stride=2)
        self.pool4 = nn.MaxPool1d(kernel_size=2, stride=2)
        self._calculate_conv_output_size()
        self.fc = nn.Linear(self.conv_output_size, num_classes)
        self.sigmoid = nn.Sigmoid()

    def _calculate_conv_output_size(self):
        dummy_input = torch.rand(1, 10, 1500) # Make sure the third value corresponds to defined sequence length
        dummy_output = self.pool1(self.conv1(dummy_input))
        dummy_output = self.pool2(self.conv2(dummy_output))
        dummy_output = self.pool3(self.conv3(dummy_output))
        dummy_output = self.pool4(self.conv4(dummy_output))
        self.conv_output_size = dummy_output.size(1) * dummy_output.size(2)

    def forward(self, x):
        x = self.pool1(self.conv1(x))
        x = self.pool2(self.conv2(x))
        x = self.pool3(self.conv3(x))
        x = self.pool4(self.conv4(x))
        x = x.view(x.size(0), -1)
        x = self.sigmoid(self.fc(x))
        return x

# Cross-Validation Setup
k_folds = 5
kf = KFold(n_splits=k_folds, shuffle=True, random_state=42)
batch_size = 64
epochs = 40
num_classes = labels_tensor.shape[1]

# Metrics Storage
fold_train_losses, fold_val_losses = [], []
fold_precisions, fold_recalls, fold_f1s, fold_mccs = [], [], [], []

print("Cross validation in progress...")

# Save the whole output in txt file
sys.stdout = open(cross_validation_path, "w")

# Cross-Validation Loop
for fold, (train_idx, val_idx) in enumerate(kf.split(kidera_encoded_sequences_tensor)):
    print(f"Fold {fold + 1}/{k_folds}")
    
    # Split data
    features_train, features_val = kidera_encoded_sequences_tensor[train_idx], kidera_encoded_sequences_tensor[val_idx]
    labels_train, labels_val = labels_tensor[train_idx], labels_tensor[val_idx]

    train_dataset = TensorDataset(features_train, labels_train)
    val_dataset = TensorDataset(features_val, labels_val)

    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)

    # Initialize model, loss, optimizer
    model = ConvolutionalNetwork(num_classes=num_classes)
    loss_fn = nn.BCELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.0001)

    # Training Loop
    train_losses, val_losses = [], []
    for epoch in range(epochs):
        model.train()
        total_train_loss = 0.0
        for batch in train_loader:
            batch_data, batch_labels = batch
            optimizer.zero_grad()
            outputs = model(batch_data)
            loss = loss_fn(outputs, batch_labels)
            loss.backward()
            optimizer.step()
            total_train_loss += loss.item()

        # Validation
        model.eval()
        total_val_loss = 0.0
        with torch.no_grad():
            for batch in val_loader:
                batch_data, batch_labels = batch
                outputs = model(batch_data)
                loss = loss_fn(outputs, batch_labels)
                total_val_loss += loss.item()

        train_losses.append(total_train_loss / len(train_loader))
        val_losses.append(total_val_loss / len(val_loader))

    # Final metrics for this fold
    model.eval()
    precision_metric = Precision(task='multilabel', num_labels=num_classes, average='weighted')
    recall_metric = Recall(task='multilabel', num_labels=num_classes, average='weighted')
    f1_metric = F1Score(task='multilabel', num_labels=num_classes, average='weighted')
    mcc_metric = MatthewsCorrCoef(task='multilabel', num_labels=num_classes)

    with torch.no_grad():
        for batch in val_loader:
            batch_data, batch_labels = batch
            outputs = model(batch_data)
            predictions = (outputs > 0.5).int()
            precision_metric.update(predictions, batch_labels.int())
            recall_metric.update(predictions, batch_labels.int())
            f1_metric.update(predictions, batch_labels.int())
            mcc_metric.update(predictions, batch_labels.int())

    precision = precision_metric.compute()
    recall = recall_metric.compute()
    f1 = f1_metric.compute()
    mcc = mcc_metric.compute()

    # Store metrics
    fold_train_losses.append(train_losses[-1])
    fold_val_losses.append(val_losses[-1])
    fold_precisions.append(precision)
    fold_recalls.append(recall)
    fold_f1s.append(f1)
    fold_mccs.append(mcc)

    print(f"Fold {fold + 1} - Train Loss: {train_losses[-1]:.4f}, Val Loss: {val_losses[-1]:.4f}")
    print(f"Precision: {precision:.4f}, Recall: {recall:.4f}, F1: {f1:.4f}, MCC: {mcc:.4f}")

# Final Aggregated Results
print("\nCross-Validation Results:")
print(f"Average Train Loss: {np.mean(fold_train_losses):.4f}")
print(f"Average Val Loss: {np.mean(fold_val_losses):.4f}")
print(f"Average Precision: {np.mean(fold_precisions):.4f}")
print(f"Average Recall: {np.mean(fold_recalls):.4f}")
print(f"Average F1 Score: {np.mean(fold_f1s):.4f}")
print(f"Average MCC: {np.mean(fold_mccs):.4f}")

# Stop recording output in the file
sys.stdout.close()
sys.stdout = sys.__stdout__

print(f"Cross validation output saved.")