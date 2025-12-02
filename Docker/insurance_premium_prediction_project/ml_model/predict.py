import pandas as pd
import pickle
import os
# a = 6
MODEL_VERSION = '1.0.0'

# print("🔍 DEBUG: __file__ =", __file__)
# print("🔍 DEBUG: dirname =", os.path.dirname(__file__))
# print("🔍 DEBUG: current working directory =", os.getcwd())
# print("🔍 DEBUG: listing current directory =", os.listdir())
# print("🔍 DEBUG: listing project root:", os.listdir("/app"))
# print("🔍 DEBUG: listing full project:", os.listdir("/app/insurance_premium_prediction_project"))
# print("🔍 DEBUG: listing ml_model folder:", os.listdir(os.path.dirname(__file__)))

# print('--------------------------')
# MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")
# print("🔍 DEBUG: MODEL_PATH =", MODEL_PATH)

try:
    with open('/app/insurance_premium_prediction_project/ml_model/model.pkl','rb') as f:
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

