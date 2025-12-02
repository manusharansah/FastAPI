from pydantic import BaseModel,Field,field_validator,computed_field
from typing import Annotated,Literal
from insurance_premium_prediction_project.config.city_tier import tier_1_cities,tier_2_cities



class UserInput(BaseModel):

    age:Annotated[int,Field(gt=0,le=120,description='Age of the person')]
    weight:Annotated[float,Field(gt=0,description='Weight of the person in kilograms(kg)')]
    height:Annotated[float,Field(gt=0,le=2.5,description='Height of the person in meters(m)')]
    income_lpa:Annotated[float,Field(gt=0,description='Annual Income of the person in Lakhs')]
    smoker:Annotated[bool,Field(description='Person is a smoker(True/False)')]
    city:Annotated[str,Field(description='City where the perosn is residing.')]
    occupation:Annotated[Literal['retired', 'freelancer', 'student', 'government_job','business_owner', 'unemployed', 'private_job'],Field(description='Work that person does for living')]



    @field_validator('city')
    @classmethod
    def transform_city(cls,v:str)->str:
        return v.strip().title()

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
