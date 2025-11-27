from fastapi import FastAPI,Path,HTTPException, Query
from fastapi.responses import JSONResponse
import json
from pydantic import BaseModel,Field,computed_field
from typing import Annotated,Literal,Optional


class Patient(BaseModel):
    id:Annotated[str,Field(...,description='ID of the patient',examples=['P001'])]
    name:Annotated[str,Field(...,description='Name of the patient')]
    city:Annotated[str,Field(...,description='City where the patient lives')]
    age:Annotated[int,Field(...,gt=0,lt=120,description='Current age of the person')]
    gender:Annotated[Literal['male','female','other'],Field(...,description='Age/Sex of the patient')]
    height:Annotated[float,Field(...,gt=0,description='Height of the patient in meters(m)')]
    weight:Annotated[float,Field(...,gt=0,description='Weighr of the patient in kilograms(kg)')]

    @computed_field
    @property
    def bmi(self)->float:
        return round(self.weight/(self.height**2),2)
    
    @computed_field
    @property
    def verdict(self)->str:
        if self.bmi<18.5:
            return 'Underwight'
        elif self.bmi>30:
            return 'Obese'
        else:
            return 'Normal'


def save_data(data):
    with open('patients.json','w') as f:
        json.dump(data,f)

def load_data():
    with open('patients.json','r') as f:
        data = json.load(f)
    return data

app = FastAPI()

@app.get('/')
def hello():
    return {'message': 'Welcome to Patient Management System (API)'}


@app.get('/about')
def about():
    return {'message': 'This is a fully functional patient management system using FastAPI'}

@app.get('/view')
def view():
    data = load_data()
    return data

@app.get('/patient/{patient_id}')
def view_patient(patient_id: str = Path(...,description='ID of the patient in the DB', example='P001')):
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404,detail='Patient not found')

@app.get('/sort')
def sorted_data(sort_by:str = Query(...,description='Sort data on the basis of height, weight or bmi',example='height'),order:str = Query('asc',description='sort in asc or desc order',example='asc')):

    sort_fields = ['height','weight','bmi']
    if sort_by  not in sort_fields:
        raise HTTPException(status_code=400,detail=f'valid sort_by values: {sort_fields}')
    if order not in ['asc','desc']:
        raise HTTPException(status_code=400,detail='valid order values: [asc,desc]')

    data = load_data()
    rev = True if order == 'desc' else False
    sorted_data = sorted(data.values(),key= lambda x: x.get(sort_by,0),reverse=rev)
    return sorted_data


@app.post('/create')
def create_pat(pat:Patient):
    data = load_data()
    if pat.id in data:
        raise HTTPException(status_code=401,detail='Patient already exists.')
    data[pat.id] = pat.model_dump(exclude={'id'})
    save_data(data)
    return JSONResponse(status_code=201,content={'message':'Patient created succssfully'})


class updatePatient(BaseModel):
    name:Annotated[Optional[str],Field(description='Name of the patient')] = None
    city:Annotated[Optional[str],Field(description='City where the patient lives')] = None
    age:Annotated[Optional[int],Field(gt=0,lt=120,description='Current age of the person')] = None
    gender:Annotated[Optional[Literal['male','female','other']],Field(description='Age/Sex of the patient')] = None
    height:Annotated[Optional[float],Field(gt=0,description='Height of the patient in meters(m)')]= None
    weight:Annotated[Optional[float],Field(gt=0,description='Weighr of the patient in kilograms(kg)')] = None

@app.put('/update/{patient_id}')
def update_pat(patient_id:str,patient:updatePatient):
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404,detail={'message':'Patient not found'})
    updated_detail = patient.model_dump(exclude_unset=True)
    existing_detail = data[patient_id]
    for key,value in updated_detail.items():
        existing_detail[key] = value
    existing_detail['id'] = patient_id
    pat = Patient(**existing_detail)
    detail = pat.model_dump(exclude=['id'])
    data[patient_id] = detail
    save_data(data)
    return JSONResponse(status_code=201,content={'message':'Record updated successfully.'})




@app.delete('/delete/{patient_id}')
def del_pat(patient_id: str):
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404,detail={'message':'Record not found'})
    del data[patient_id]
    save_data(data)
    return JSONResponse(status_code=204,content={'message':'Record deleted successfully'})