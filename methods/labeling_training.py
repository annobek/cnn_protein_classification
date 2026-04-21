from sklearn.preprocessing import MultiLabelBinarizer
import pandas as pd
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset, random_split
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import precision_score, recall_score, f1_score, matthews_corrcoef
from sklearn.model_selection import train_test_split
from torchmetrics.classification import Precision, Recall, F1Score, MatthewsCorrCoef
import sys 
import os

# Paths to the used files
cleaned_sequences_path = os.path.join("..", "results", "NEW_labeled_sequences.csv")
kidera_encoded_path = os.path.join("..", "results", "kidera_encoded_compressed.npz")
training_output_path = os.path.join("..", "results", "training_output.txt")
training_validation_path = os.path.join("..", "results", "training_validation_loss.png")

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

# Data preparation for training
kidera_encoded_sequences_tensor = torch.tensor(kidera_encoded_sequences, dtype=torch.float32)
labels_tensor = torch.tensor(bincode_encoded, dtype=torch.float32)  # labels are converted to float for BCE loss

# Permute the tensor to [num_sequences, num_features, sequence_length]
kidera_encoded_sequences_tensor = kidera_encoded_sequences_tensor.permute(0, 2, 1)


# Random data split step 

labels = labels_tensor.numpy()

# sum of labels across all samples for each class
label_sums = labels.sum(axis=0) # computes the sum of 1s along the rows

# Create indices and shuffle them
indices = np.arange(len(labels))

np.random.seed(42)
np.random.shuffle(indices)

# Split
split_point = int(0.8 * len(labels))  # 80-20 split
train_indices = indices[:split_point]
val_indices = indices[split_point:]

features_train, features_val = kidera_encoded_sequences_tensor[train_indices], kidera_encoded_sequences_tensor[val_indices]
labels_train, labels_val = labels_tensor[train_indices], labels_tensor[val_indices]

# Convert back to PyTorch tensors
features_train_tensor = torch.tensor(features_train, dtype=torch.float32)
features_val_tensor = torch.tensor(features_val, dtype=torch.float32)
labels_train_tensor = torch.tensor(labels_train, dtype=torch.float32)
labels_val_tensor = torch.tensor(labels_val, dtype=torch.float32)


# Create TensorDatasets
train_dataset = TensorDataset(features_train_tensor, labels_train_tensor)
val_dataset = TensorDataset(features_val_tensor, labels_val_tensor)

# DataLoaders for batching
batch_size = 64
train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)

print("Training in progress...")

# Save the whole output in txt file
sys.stdout = open(training_output_path, "w")

print(f"Train set size: {len(train_dataset)}")
print(f"Validation set size: {len(val_dataset)}")

num_classes = labels_tensor.shape[1]

# CNN Model defined (uncomment on lines 96, 99, 102, 105, 110, 128, 131, 134, 137 and 139 to add dropout layers if needed)

class ConvolutionalNetwork(nn.Module):
    def __init__(self):
        super(ConvolutionalNetwork, self).__init__()
        self.conv1 = nn.Conv1d(in_channels=10, out_channels=32, kernel_size=7, stride=2)
        self.pool1 = nn.MaxPool1d(kernel_size=2, stride=2)
        #self.dropout1 = nn.Dropout(p=0.2)  # First dropout layer
        self.conv2 = nn.Conv1d(in_channels=32, out_channels=64, kernel_size=5, stride=2)
        self.pool2 = nn.MaxPool1d(kernel_size=2, stride=2)
        #self.dropout2 = nn.Dropout(p=0.2)  # Second dropout layer
        self.conv3 = nn.Conv1d(in_channels=64, out_channels=128, kernel_size=3, stride=2)
        self.pool3 = nn.MaxPool1d(kernel_size=2, stride=2)
        #self.dropout3 = nn.Dropout(p=0.2)  # Third dropout layer
        self.conv4 = nn.Conv1d(in_channels=128, out_channels=256, kernel_size=3, stride=2)
        self.pool4 = nn.MaxPool1d(kernel_size=2, stride=2)
        #self.dropout4 = nn.Dropout(p=0.2)  # Fourth dropout layer

        self._calculate_conv_output_size()
        
        self.fc = nn.Linear(self.conv_output_size, num_classes)
        #self.fc_dropout = nn.Dropout(p=0.5)  # Dropout before fully connected layer
        self.sigmoid = nn.Sigmoid()  

    def _calculate_conv_output_size(self):
        dummy_input = torch.rand(1, 10, 1500)  # Make sure the third value corresponds to defined sequence length 
        dummy_output = self.conv1(dummy_input)
        dummy_output = self.pool1(dummy_output)
        dummy_output = self.conv2(dummy_output)
        dummy_output = self.pool2(dummy_output)
        dummy_output = self.conv3(dummy_output)
        dummy_output = self.pool3(dummy_output)
        dummy_output = self.conv4(dummy_output)
        dummy_output = self.pool4(dummy_output)
        self.conv_output_size = dummy_output.size(1) * dummy_output.size(2)

    def forward(self, x):
        x = self.conv1(x)
        x = self.pool1(x) 
        #x = self.dropout1(x) 
        x = self.conv2(x)
        x = self.pool2(x) 
        #x = self.dropout2(x) 
        x = self.conv3(x)
        x = self.pool3(x)
        #x = self.dropout3(x) 
        x = self.conv4(x)
        x = self.pool4(x)
        #x = self.dropout4(x) 
        x = x.view(x.size(0), -1)
        #x = self.fc_dropout(x) 
        x = self.fc(x)
        x = self.sigmoid(x)
        return x


# Model, loss function, and optimizer initialisation
model = ConvolutionalNetwork()
loss_fn = nn.BCELoss()

# Adjust this part for different optimizers, learning rates and weight decay if needed.
# Add weight_decay=1e-4 after defining the learning rate.
optimizer = torch.optim.Adam(model.parameters(), lr=0.0001) 

# Training
epochs = 40 
train_losses = []
val_losses = []

# Measure training time
start_event = torch.cuda.Event(enable_timing=True)
end_event = torch.cuda.Event(enable_timing=True)

start_event.record()  # Start timing

for epoch in range(epochs):
    model.train()
    total_train_loss = 0.0

    # Training loop
    for batch in train_loader:
        batch_data, batch_labels = batch
        optimizer.zero_grad()
        outputs = model(batch_data)
        loss = loss_fn(outputs, batch_labels)
        loss.backward()
        optimizer.step()
        total_train_loss += loss.item()

    # Validation loop
    model.eval()
    total_val_loss = 0.0
    with torch.no_grad():
        for batch in val_loader:
            batch_data, batch_labels = batch
            outputs = model(batch_data)
            loss = loss_fn(outputs, batch_labels)
            total_val_loss += loss.item()

    # Average losses
    train_loss = total_train_loss / len(train_loader)
    val_loss = total_val_loss / len(val_loader)
    train_losses.append(train_loss)
    val_losses.append(val_loss)

    print(f"Epoch {epoch+1}/{epochs} - Train Loss: {train_loss:.4f}, Val Loss: {val_loss:.4f}")

end_event.record()  # End timing
torch.cuda.synchronize()  # Ensure CUDA operations are completed

# Calculate elapsed time
elapsed_time = start_event.elapsed_time(end_event) / 1000  # Convert to seconds
elapsed_time_minutes = elapsed_time / 60  # Convert seconds to minutes

print(f"Total training time: {elapsed_time_minutes:.2f} minutes")    
    
# Metric calculation after all epochs
print("\nCalculating metrics on the validation set...")

# Metrics initialization
precision_metric = Precision(task='multilabel', num_labels=num_classes, average='weighted')
recall_metric = Recall(task='multilabel', num_labels=num_classes, average='weighted')
f1_metric = F1Score(task='multilabel', num_labels=num_classes, average='weighted')
mcc_metric = MatthewsCorrCoef(task='multilabel', num_labels=num_classes)

y_test = []
y_pred = []

# Evaluate metrics on validation set
model.eval()
precision_metric.reset()
recall_metric.reset()
f1_metric.reset()
mcc_metric.reset()

with torch.no_grad():
    for batch in val_loader:
        batch_data, batch_labels = batch
        outputs = model(batch_data)
        predictions = (outputs > 0.5).int()  # Convert probabilities to binary and integer type
        batch_labels = batch_labels.int()   # Ensure labels are also integers
        y_test.extend(batch_labels.cpu().numpy())
        y_pred.extend(predictions.cpu().numpy())

        
        # Update metrics with predictions and true labels
        precision_metric.update(predictions, batch_labels)
        recall_metric.update(predictions, batch_labels)
        f1_metric.update(predictions, batch_labels)
        mcc_metric.update(predictions, batch_labels)
        
y_test = np.array(y_test)
y_pred = np.array(y_pred)

# Number of classes
print("Number of classes:", num_classes)

# Compute and display metrics
precision = precision_metric.compute()
recall = recall_metric.compute()
f1 = f1_metric.compute()
mcc = mcc_metric.compute()

# Calculate accuracy manually to compare with metrics provided with torch
y_pred_class = y_pred.argmax(axis=1)  # Select the highest-probability class
y_true_class = y_test.argmax(axis=1)
accuracy = (y_pred_class == y_true_class).mean()
print(f"Accuracy: {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall: {recall:.4f}")
print(f"F1 Score: {f1:.4f}")
print(f"MCC: {mcc:.4f}")

# Plot training and validation loss
plt.plot(range(1, epochs + 1), train_losses, label='Train Loss')
plt.plot(range(1, epochs + 1), val_losses, label='Validation Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.title('Training and Validation Loss')
plt.legend()
plt.savefig(training_validation_path)

# Stop recording output in the file
sys.stdout.close()
sys.stdout = sys.__stdout__

print(f"Training output saved.")
print(f"Training and validation loss graphs saved.")