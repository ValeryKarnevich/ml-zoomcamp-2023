import pickle

with open('model1.bin', 'rb') as model_file, open('dv.bin', 'rb') as dv_file:
    model = pickle.load(model_file)
    dv = pickle.load(dv_file)

def predict(customer):
    X = dv.transform([customer])
    y_pred = model.predict_proba(X)[0, 1]
    is_credit = y_pred >= 0.5

    result = {
        'credit_probability': float(y_pred),
        'credit': bool(is_credit)
    }

    return result
