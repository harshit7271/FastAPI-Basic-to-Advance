import json
from fastapi import FastAPI, Path, HTTPException, Query
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal

app = FastAPI()
# post
class Patient(BaseModel):
    
    id: Annotated[str, Field(..., description= 'ID of the Patient', examples=['P001'])]
    name : Annotated[str, Field(..., description= 'Name of the patient')]
    city : Annotated[str, Field(..., description= 'City where the patient live')]
    age : Annotated[int, Field(..., gt =0, lt = 120, description='Age of the patient')]
    gender : Annotated[Literal['male', 'female', 'other'], Field(..., description =  'Gender of the patient')]
    height : Annotated[float, Field(..., gt = 0, description= 'Hieght of the patient in mtrs')]
    weight : Annotated[float, Field(..., gt = 0, description= 'Weight of the patient in kg')]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight/(self.height)**2, 2)   # rounding off bmi to two digits
        return bmi
    
    
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

# PATH PARAMETER

@app.get('/view_patient/{patient_id}')

def view_patient(patient_id: str = Path(..., description="The ID of the patient to retrieve", example="P001")):
    # load all patient data
    data = load_data()

    if patient_id in data:
        return {'data': data[patient_id]}
    raise HTTPException(status_code=404, detail="Patient not found")     # if patient_id not in data it will raise 404 error

# Endpoint to sort patients by querry parameter

@app.get('/sort')
def sort_patients(sort_by: str = Query(..., description='Sort on the basis of height, weight or bmi'), order: str = Query('asc', description='sort in asc or desc order')):

    valid_fields = ['height', 'weight', 'bmi']

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f'Invalid field select from {valid_fields}')
    
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail='Invalid order select between asc and desc')
    
    data = load_data()

    sort_order = True if order=='desc' else False

    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=sort_order)

    
    return sorted_data
 




