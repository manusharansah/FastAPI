import pandas as pd
import pickle


MODEL_VERSION = '1.0.0'


try:
    with open('ml_model/model.pkl','rb') as f:
        model = pickle.load(f)
except:
    model = None
if model is not None:
    classes = model.classes_.tolist()

def predict_ouptut(user_input: dict):
    input_df = pd.DataFrame([user_input])
    category = model.predict(input_df)[0]
    probabilities = model.predict_proba(input_df)[0]
    classes_prob = dict(zip(classes,map(lambda p: round(p,4),probabilities)))
    output = {'predicted_category': category,'Category_Confidence_Scores':classes_prob}
    return output

