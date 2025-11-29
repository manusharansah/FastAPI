from fastapi import FastAPI
from fastapi.responses import JSONResponse
from schema.user_input import UserInput
from ml_model.predict import MODEL_VERSION,model,predict_ouptut

app = FastAPI()

@app.get('/')
def home():
    return {'message':'Welcome to Insurance Category Prediuction Model'}


@app.get('/health')
def health():
    return {
        'status':'OK',
        'version': MODEL_VERSION,
        'model_loaded':  model is not None 
        }



@app.post('/predict')
def predict(data:UserInput):
    user_input = {
        'age_group' : data.age_group,
        'bmi' : data.bmi,
        'lifestyle_risk': data.lifestyle_risk,
        'city_tier' : data.city_tier,
        'income_lpa' : data.income_lpa,
        'occupation' : data.occupation
    }


    if model is None:
        return JSONResponse(status_code=500,content={'message':'Model Failed to Load'})
    try:
        output = predict_ouptut(user_input)
        return JSONResponse(status_code=200,content={'predicted_insurance_premium_category':output['predicted_category'],'category_confidence_scores':output['Category_Confidence_Scores']})
    except Exception as e:
        return JSONResponse(status_code=400,content={'detail':f'Error during prediction. Error: {e}'})