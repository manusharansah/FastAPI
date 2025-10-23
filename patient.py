from fastapi import FastAPI,Path,HTTPException, Query
import json

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
    rev = True if order == 'asc' else False
    sorted_data = sorted(data.values(),key= lambda x: x.get(sort_by,0),reverse=rev)
    return sorted_data
