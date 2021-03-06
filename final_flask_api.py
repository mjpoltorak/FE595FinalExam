import flask
import pickle
import pandas as pd

app = flask.Flask(__name__)


def pickle_predict(type, params):
    # Checks which type of model to run and then loads the pickled file and predicts with the given input
    try:
        params_df = pd.DataFrame(params, index=[1])
        if type == 'logistic':
            with open('logistic_regression.pkl', 'rb') as file:
                logistic = pickle.load(file)
                prob = logistic.predict(params_df)
        elif type == 'svm':
            with open('svm.pkl', 'rb') as file:
                svm = pickle.load(file)
                prob = svm.predict(params_df)
        elif type == 'random_forest':
            with open('rf.pkl', 'rb') as file:
                rf = pickle.load(file)
                prob = rf.predict(params_df)
        elif type == 'knn':
            with open('knn.pkl', 'rb') as file:
                knn = pickle.load(file)
                prob = knn.predict(params_df)
        return prob

    except:
        return 'Error occurred in prediction'


@app.route('/help', methods=['GET'])
def help():
    return flask.render_template("help.html")


@app.route('/predict', methods=['POST'])
def predict():
    # Get all data from POST json
    post_json = flask.request.json
    type = post_json.get('type', 'random_forest')
    receipts = post_json.get('receipts', None)
    disbursements = post_json.get('disbursements', None)
    cash_on_hand_end_period = post_json.get('cash_on_hand_end_period', None)
    debts_owed_by_committee = post_json.get('debts_owed_by_committee', None)
    num_terms = post_json.get('num_terms', None)
    # check if all required data is present
    if receipts is not None and disbursements is not None and cash_on_hand_end_period is not None and \
            debts_owed_by_committee is not None and num_terms is not None:
        params = {'receipts': receipts,'disbursements': disbursements,
                  'cash_on_hand_end_period': cash_on_hand_end_period,'debts_owed_by_committee': debts_owed_by_committee,
                  'num_terms': num_terms}
        res = pickle_predict(type, params)
        return {'success': True, 'response': {'prediction': str(res[0])}}
    else:
        return {'success': False, 'error': 'Missing arugment from json payload'}, 400


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8081)
