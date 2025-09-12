import json
from fastapi import FastAPI

app = FastAPI()

def load_data():
    with open('patients.json', 'r') as f:
        data = json.load(f)

    return data
       

@app.get("/")
def hello():
    return {'Patient Management System'}

@app.get('/about')
def about():
    return {'Message': 'This is a Patient Management System API built with FastAPI.'}

@app.get('/view_patients')
def view_patients():
    data = load_data()
    return {'data': data}

