from fastapi import FastAPI

app = FastAPI()

@app.get('/')       # end-point
def hello():
    return {'message': 'Habibi, Ham tumko hi bolti'}

@app.get('/joke')       # another end-point
def joke():
    return {'message': 'Hum joke sunane ke mood me nahi hoti'}

@app.get('/about')
def about():
    return {'message': 'Hum habibibi bolti'}