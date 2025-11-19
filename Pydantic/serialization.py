from pydantic import BaseModel

class Address(BaseModel):
    city:str
    district:str
    pincode:str

class Patient(BaseModel):
    name:str
    age:int
    address:Address

def display(pat:Patient):
    print('Patient Data')
    print(pat.name)
    print(pat.age)
    print(pat.address)


address_data = {'city':'Janakpur','district':'Dharan','pincode':'U5679'}
address1 = Address(**address_data)

pat_data = {'name':'Manu','age':21,'address':address1}
pat = Patient(**pat_data)

display(pat)

#serialization
temp = pat.model_dump()
print(temp)

#custom serialization
temp1 = pat.model_dump(exclude={'address':{'district'},'age':...})
print(temp1)

#serialization with JSON
temp3 = pat.model_dump_json()
print(temp3)
