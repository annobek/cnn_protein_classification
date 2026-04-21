import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

data = pd.read_csv("embedded_proteins.csv", nrows = 10000)

x = data.drop(columns=["family"]).values
y = data["family"] #extract family column as target
#print(x)
#print(y)

#encode family labels into numerical format
encoding = LabelEncoder()
y_encoded = encoding.fit_transform(y)

#print("feature shape: " , x.shape)
#print("endoded labels shape: ", y_encoded.shape)

#Splitting data into tarining and testing sets
x_train, x_test, y_train, y_test = train_test_split(x, y_encoded, test_size=0.2, random_state=42) #20% of data will be used for test and 80% for training

#print("Training set size", x_train.shape[0])
#print("Test set size", x_test.shape[0])

#train model:

#scale data:
# Scale the features
scaler = StandardScaler()
x_train_scaled = scaler.fit_transform(x_train)
x_test_scaled = scaler.transform(x_test)

#logistic regression as baseline:

logistic_model = LogisticRegression(max_iter=5000, random_state = 42, multi_class='ovr', solver = 'lbfgs',class_weight='balanced')
#multiclass classification problem (protein families)
logistic_model.fit(x_train_scaled, y_train)

#evaluate model:

from sklearn.metrics import classification_report, matthews_corrcoef

# Make predictions
y_pred = logistic_model.predict(x_test)  #
# Classification report
#print(classification_report(y_test, y_pred, target_names=encoding.classes_))

# Matthews Correlation Coefficient
mcc = matthews_corrcoef(y_test, y_pred)
print("Matthews Correlation Coefficient:", mcc)
unique_classes = sorted(set(y_test))  # Or use `np.unique(y_test)` to get the class labels
print("Unique classes in y_test:", unique_classes)
print("Unique classes in y_pred:", sorted(set(y_pred)))

print(classification_report(y_test, y_pred, labels=unique_classes))

print("Class distribution in y_train:", pd.Series(y_train).value_counts())
