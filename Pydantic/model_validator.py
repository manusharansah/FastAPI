from pydantic import BaseModel,model_validator
from typing import Dict,Any


class Patient(BaseModel):
    name:str
    age:int
    contact: Dict[str,Any]

    @model_validator(mode='after')
    def model_validate(cls,model):
        if model.age>60 and 'emergency' not in model.contact:
            raise ValueError('Senior citizen must have emergency contact')
        return model

def display(pat:Patient):
    print('Displaying the details of the patient')
    print('Name: ',pat.name)
    print('Email: ',pat.email)
    print('Age: ',pat.age)
    return None

pat_info = {'name':'Saroj','email':'saroj123@gmail.com','age':70,'contact':{'phone':'+977-9863483016'}}
# This statement will raise a ValueError

pat = Patient(**pat_info)

display(pat)
