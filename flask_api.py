import flask
import pickle
import pandas as pd

app = flask.Flask(__name__)


def pickle_predict(type, params):
    try:
        if type == 'logistic':
            with open('logistic_regression.pkl', 'rb') as file:
                logistic = pickle.load(file)
                params_df = pd.DataFrame(params, index=[1])
                prob = logistic.predict(params_df)
        return prob

    except:
        return 'Error occurred in prediction'


@app.route('/help', methods=['GET'])
def help():
    return flask.render_template("help.html")


@app.route('/predict', methods=['POST'])
def predict():
    post_json = flask.request.json
    type = post_json.get('type', 'logistic')
    receipts = post_json.get('receipts', None)
    disbursements = post_json.get('disbursements', None)
    cash_on_hand_end_period = post_json.get('cash_on_hand_end_period', None)
    debts_owed_by_committee = post_json.get('debts_owed_by_committee', None)
    num_terms = post_json.get('num_terms', None)
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
