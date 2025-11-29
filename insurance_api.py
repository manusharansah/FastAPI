from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field,computed_field
from typing import Annotated,Literal
import pandas as pd
import pickle

try:
    with open('model.pkl','rb+') as f:
        model = pickle.load(f)
except:
    model = None
    



tier_1_cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune"]
tier_2_cities = [
    "Jaipur", "Chandigarh", "Indore", "Lucknow", "Patna", "Ranchi", "Visakhapatnam", "Coimbatore",
    "Bhopal", "Nagpur", "Vadodara", "Surat", "Rajkot", "Jodhpur", "Raipur", "Amritsar", "Varanasi",
    "Agra", "Dehradun", "Mysore", "Jabalpur", "Guwahati", "Thiruvananthapuram", "Ludhiana", "Nashik",
    "Allahabad", "Udaipur", "Aurangabad", "Hubli", "Belgaum", "Salem", "Vijayawada", "Tiruchirappalli",
    "Bhavnagar", "Gwalior", "Dhanbad", "Bareilly", "Aligarh", "Gaya", "Kozhikode", "Warangal",
    "Kolhapur", "Bilaspur", "Jalandhar", "Noida", "Guntur", "Asansol", "Siliguri"
]



class UserInput(BaseModel):

    age:Annotated[int,Field(gt=0,le=120,description='Age of the person')]
    weight:Annotated[float,Field(gt=0,description='Weight of the person in kilograms(kg)')]
    height:Annotated[float,Field(gt=0,le=2.5,description='Height of the person in meters(m)')]
    income_lpa:Annotated[float,Field(gt=0,description='Annual Income of the person in Lakhs')]
    smoker:Annotated[bool,Field(description='Person is a smoker(True/False)')]
    city:Annotated[str,Field(description='City where the perosn is residing.')]
    occupation:Annotated[Literal['retired', 'freelancer', 'student', 'government_job','business_owner', 'unemployed', 'private_job'],Field(description='Work that person does for living')]


    @computed_field
    @property
    def bmi(self)->float:
        return self.weight/(self.height**2)
    
    @computed_field
    @property
    def lifestyle_risk(self)->str:
        smoker = self.smoker
        bmi = self.bmi
        if smoker and (bmi > 25 or bmi < 18.5):
            return 'High'
        elif smoker or bmi > 25 or bmi < 18.5:
            return 'Medium'
        else:
            return 'Low'
        

    @computed_field
    @property
    def age_group(self)->str:
        if self.age<25:
            return 'young'
        elif self.age<60:
            return 'adult'
        else: 
            return 'senior-citizen'
    

    @computed_field
    @property
    def city_tier(self)->int:
        if self.city in tier_1_cities:
            return 1
        elif self.city in tier_2_cities:
            return 2
        else:
            return 3






app = FastAPI()

@app.get('/')
def home():
    return {'message':'Welcome to Insurance Category Prediuction Model'}

@app.post('/predict')
def predict(data:UserInput):
    input_df = pd.DataFrame([{
        'age_group' : data.age_group,
        'bmi' : data.bmi,
        'lifestyle_risk': data.lifestyle_risk,
        'city_tier' : data.city_tier,
        'income_lpa' : data.income_lpa,
        'occupation' : data.occupation
    }])
 

    if model is None:
        return JSONResponse(status_code=500,content={'message':'Model Failed to Load'})
    try:
        prediction = model.predict(input_df)[0]
        return JSONResponse(status_code=200,content={'predicted_insurance_premium_category':prediction})
    except Exception as e:
        return JSONResponse(status_code=400,content={'detail':f'Error during prediction. Error: {e}'})