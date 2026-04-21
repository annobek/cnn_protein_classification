import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
#Load the Dataset for an overview

data = pd.read_csv("embedded_proteins.csv")
#check data structure:
#print(data.head())

#Prepare features (kidera) and Labels(family)

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

#logistic regression as baseline:

logistic_model = LogisticRegression(max_iter=1000, random_state = 42, multi_class='multinomial', solver = 'lbfgs')
#multiclass classification problem (protein families)
logistic_model.fit(x_train, y_train)

#evaluate model:

from sklearn.metrics import classification_report, matthews_corrcoef

# Make predictions
y_pred = logistic_model.predict(x_test)  #
# Classification report
print(classification_report(y_test, y_pred, target_names=encoding.classes_))

# Matthews Correlation Coefficient
mcc = matthews_corrcoef(y_test, y_pred)
print("Matthews Correlation Coefficient:", mcc)
