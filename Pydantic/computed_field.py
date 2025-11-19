from pydantic import BaseModel,computed_field

class Patient(BaseModel):
    name:str
    height:float
    weight:float

    @computed_field
    @property
    def bmi(self)->float:
        return round((self.weight)/(self.height**2),2)
    
def display(pat:Patient):
    print('Displaying the details of the patient')
    print('Name: ',pat.name)
    print('Weight: ',pat.weight)
    print('Height: ',pat.height)
    print('BMI: ',pat.bmi)
    return None

pat_info = {'name':'Manu','weight':70,'height':1.72}

pat = Patient(**pat_info)

display(pat)