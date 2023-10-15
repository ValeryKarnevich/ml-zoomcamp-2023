import pickle
from flask import Flask
from flask import request
from flask import jsonify

model_file_name = 'model2.bin'
dv_file_name = 'dv.bin'

with open(model_file_name, 'rb') as model_file, open(dv_file_name, 'rb') as dv_file:
    model = pickle.load(model_file)
    dv = pickle.load(dv_file)

app = Flask('credit')

@app.route('/predict_credit', methods=['POST'])
def predict():
    customer = request.get_json()

    X = dv.transform([customer])
    y_pred = model.predict_proba(X)[0, 1]
    is_credit = y_pred >= 0.5

    result = {
        'credit_probability': float(y_pred),
        'credit': bool(is_credit)
    }

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9696)