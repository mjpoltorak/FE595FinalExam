import pandas as pd
import pickle
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn import svm
from sklearn.svm import LinearSVC

data = pd.read_csv("subset_cleaned_election_data.csv")
data = data.dropna()
target = data['win']
data = data[['receipts', 'disbursements', 'cash_on_hand_end_period', 'debts_owed_by_committee', 'num_terms']]

x_train, x_test, y_train, y_test = train_test_split(data, target, test_size=0.3, random_state=4)

# Logistic Regression
logit = LogisticRegression().fit(x_train, y_train)
prediction = logit.predict(x_test)
print(accuracy_score(y_test, prediction))


filename = 'logistic_regression.pkl'
model_pkl = open(filename,'wb')
pickle.dump(logit, model_pkl)
model_pkl.close()

# Support Vector Machines - Linear Kernel
clf = LinearSVC(random_state=0, tol=1e-5, penalty='l2', loss='squared_hinge').fit(x_train, y_train)
prediction = clf.predict(x_test)
print(accuracy_score(y_test, prediction))

filename = 'svm.pkl'
svm_pkl = open(filename, 'wb')
pickle.dump(clf, svm_pkl)
svm_pkl.close()
