# FE595FinalExam

### Accuracy Scores of the Respective Models Used
#### Logistic Regression
Accuracy Rate: 78.95%

#### Support Vector Machine - Linear Support Vector Classification
Accuracy Rate: 66.16%

#### K Nearest Neighbors (with k = 7)
Accuracy Rate: 86.15%

#### Random Forest (n_trees 100, max_depth = 5)
Accuracy Rate: 91.01%

We used the following variables to train the ML models:
['receipts','disbursements','cash_on_hand_end_period','debts_owed_by_committee','percent_vote','num_terms']

Based on the results shown above, all models produced impressive results, but the best model was the random forest classifier

The models can be used to predict new input using a POST at http://ec2-18-191-182-78.us-east-2.compute.amazonaws.com:8081/predict

The instructions for using the API can be found at http://ec2-18-191-182-78.us-east-2.compute.amazonaws.com:8081/help

The data was cleaned using the data_clean.py code.
The models were trained using teh models.py code.