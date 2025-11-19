from pydantic import BaseModel,EmailStr,field_validator


class Patient(BaseModel):
    name:str
    email:EmailStr
    age:int


    #field-validator for custom data validation
    @field_validator('email')
    @classmethod
    def validate_email(cls,val):
        valid_domains = ['gmail.com','yahoo.com']
        domain_name = val.split('@')[-1]
        if domain_name not in valid_domains:
            raise ValueError('Not a valid domain for email')
        return val
    
    #field-validator for custom data transformation
    @field_validator('name')
    @classmethod
    def modify_name(cls,val):
        return val.lower()


def display(pat:Patient):
    print('Displaying the details of the patient')
    print('Name: ',pat.name)
    print('Email: ',pat.email)
    print('Age: ',pat.age)
    return None

pat_info = {'name':'Manu','email':'manu1saurabh@gmail.com','age':21}

pat = Patient(**pat_info)

display(pat)