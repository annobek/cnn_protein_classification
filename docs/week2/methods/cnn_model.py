import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset, random_split
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, classification_report, matthews_corrcoef

'''
Simulate the dataset
kidera_encoded_sequences = np.random.rand(41669, 256, 10)
labels = np.random.randint(0, 10, size=(41669,))  # Simulated labels (10 classes)
'''

# Convrt to PyTorch tensors
kidera_encoded_sequences_tensor = torch.tensor(kidera_encoded_sequences, dtype=torch.float32)
labels_tensor = torch.tensor(bincode_encoded, dtype=torch.long)

# Permute the tensor to [num_sequences, num_features, sequence_length]
kidera_encoded_sequences_tensor = kidera_encoded_sequences_tensor.permute(0, 2, 1)

# Split the dataset into training and validation sets
dataset = TensorDataset(kidera_encoded_sequences_tensor, labels_tensor)
train_size = int(0.8 * len(dataset))
val_size = len(dataset) - train_size
train_dataset, val_dataset = random_split(dataset, [train_size, val_size])

#DataLoaders for batching
batch_size = 32 #adjust as necessary for different batches
train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)


#print(f"Max label: {labels_tensor.max()}, Min label: {labels_tensor.min()}")

num_classes = len(np.unique(labels_tensor))  #number of unique labels
#print(num_classes)

# CNN model
class ConvolutionalNetwork(nn.Module):
    def __init__(self):
        super(ConvolutionalNetwork, self).__init__()
        self.conv1 = nn.Conv1d(in_channels=10, out_channels=32, kernel_size=7, stride=2)
        self.conv2 = nn.Conv1d(in_channels=32, out_channels=64, kernel_size=5, stride=2)
        self.conv3 = nn.Conv1d(in_channels=64, out_channels=128, kernel_size=3, stride=2)
        self.conv4 = nn.Conv1d(in_channels=128, out_channels=256, kernel_size=3, stride=2)
        self._calculate_conv_output_size()
        self.fc = nn.Linear(self.conv_output_size, num_classes)



    def _calculate_conv_output_size(self):
        dummy_input = torch.rand(1, 10, 256)  # Simulate a single input
        dummy_output = self.conv1(dummy_input)
        dummy_output = self.conv2(dummy_output)
        dummy_output = self.conv3(dummy_output)
        dummy_output = self.conv4(dummy_output)
        self.conv_output_size = dummy_output.size(1) * dummy_output.size(2)

    def forward(self, x):
        x = self.conv1(x)
        x = self.conv2(x)
        x = self.conv3(x)
        x = self.conv4(x)
        x = x.view(x.size(0), -1)  # Flatten the output
        x = self.fc(x)
        return x

# Initialize the model, loss function, and optimizer
model = ConvolutionalNetwork()
loss_fn = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

# Training
epochs = 100
train_losses = []
val_losses = []
for epoch in range(epochs):
    model.train()  # Set model to training mode
    total_train_loss = 0.0

    for batch in train_loader:
        batch_data, batch_labels = batch
        optimizer.zero_grad()  # Clear gradients
        outputs = model(batch_data)  # Forward pass
        loss = loss_fn(outputs, batch_labels)  # Compute loss
        loss.backward()  # Backpropagation
        optimizer.step()  # Update weights
        total_train_loss += loss.item()

# Evaluate on validation
    model.eval()  # Set model to evaluation mode
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

# Get true labels and predictions
y_test = []
y_pred = []

model.eval()  # Set the model to evaluation mode
with torch.no_grad():
    for batch in val_loader:
        batch_data, batch_labels = batch
        outputs = model(batch_data)
        _, predicted = torch.max(outputs, dim=1)  # Get class index with max probability
        y_test.extend(batch_labels.cpu().numpy())
        y_pred.extend(predicted.cpu().numpy())

y_test = np.array(y_test)
y_pred = np.array(y_pred)

# Matthews Correlation Coefficient
mcc = matthews_corrcoef(y_test, y_pred)
print("Matthews Correlation Coefficient:", mcc)

print("Unique classes in y_test:", len(set(y_test)))
print("Unique classes in y_pred:", len(set(y_pred)))


# Visualization
plt.plot(range(1, epochs + 1), train_losses, label='Train Loss')
plt.plot(range(1, epochs + 1), val_losses, label='Validation Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.title('Training and Validation Loss')
plt.legend()
plt.show()

