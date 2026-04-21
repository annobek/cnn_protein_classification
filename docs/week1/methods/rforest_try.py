import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report


data = pd.read_csv("embedded_proteins.csv", nrows = 20000)

x = data.drop(columns=["family"]).values
y = data["family"] #extract family column as target
#print(x)
#print(y)

#encode family labels into numerical format
encoding = LabelEncoder()
y_encoded = encoding.fit_transform(y)

#Splitting data into tarining and testing sets
x_train, x_test, y_train, y_test = train_test_split(x, y_encoded, test_size=0.2, random_state=42) #20% of data will be used for test and 80% for training

#scale data:
# Scale the features
scaler = StandardScaler()
x_train_scaled = scaler.fit_transform(x_train)
x_test_scaled = scaler.transform(x_test)

random_forest = RandomForestClassifier(n_estimators=200, random_state = 42, class_weight='balanced')
#multiclass classification problem (protein families)
random_forest.fit(x_train_scaled, y_train)

#evaluate model:

from sklearn.metrics import classification_report, matthews_corrcoef

# Make predictions
y_pred = random_forest.predict(x_test)  #
# Classification report
#print(classification_report(y_test, y_pred, target_names=encoding.classes_))

# Matthews Correlation Coefficient
mcc = matthews_corrcoef(y_test, y_pred)
print("Matthews Correlation Coefficient:", mcc)
unique_classes = sorted(set(y_test)) 
print("Unique classes in y_test:", unique_classes)
print("Unique classes in y_pred:", sorted(set(y_pred)))


#print(data.isnull().sum()) 
print("Class distribution in y_train:", pd.Series(y_train).value_counts())
# Evaluate accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy}")


#print("Classification report: ", classification_report(y_test, y_pred,labels=unique_classes, output_dict=True))

#report_dict = classification_report(y_test, y_pred,labels=unique_classes, output_dict=True)
#class_report = pd.DataFrame(report_dict)

#class_report.to_markdown("Classification_report.md")