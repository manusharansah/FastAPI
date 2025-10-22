from fastapi import FastAPI
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