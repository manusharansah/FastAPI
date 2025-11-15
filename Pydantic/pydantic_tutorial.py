#Ptydantic model

from pydantic import BaseModel,EmailStr,Field
from typing import Optional,Annotated, Dict

class Patient(BaseModel):
    name: Annotated[str,Field(max_length=50)]
    age: int = Field(gt=0,le=120)
    weight: float 
    married: bool = False
    email: Optional[EmailStr] = None
    allergies : Annotated[Optional[Dict[str,str]],Field(default=None)]


def insert(pat:Patient):
    print(pat.name)
    print(pat.age)
    print('insertion successful')

pat_info = {'name': 'Manu', 'age':20,'weight':65,'email':'manu1saurabh@gmail.com'}
pat = Patient(**pat_info)
insert(pat)