from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
import pymongo
import dotenv
import os

dotenv.load_dotenv()

app = FastAPI()


class Employee(BaseModel):
    id: int
    name: str
    email: str
    profession: str
    level: str


class EmployeeUpdate(BaseModel):
    id: int
    name: Optional[str]
    email: Optional[str]
    profession: Optional[str]
    level: Optional[str]


def get_db(db_name="EmployeeDB"):
    client = pymongo.MongoClient(os.getenv("MONGO_URL"))
    db = client.get_database(db_name)
    return db


@app.get("/")
def home():
    return {"message": "Welcome Home!!"}


@app.get("/employee/{id}", response_model=Employee)
def get_employee(id: int):
    db = get_db()
    col = db.get_collection("Employee")
    emp = col.find_one({"id": id})
    return emp


@app.post("/employee")
def create_employee(data: Employee):
    db = get_db()
    col = db.get_collection("Employee")

    new_emp = col.insert_one(data.dict())
    if new_emp.acknowledged:
        return {"message": f"Employee {data.name} created"}
    return {"message": "error occured while creating employee"}


@app.put("/employee")
def update_employee(data: EmployeeUpdate):
    db = get_db()
    col = db.get_collection("Employee")
    emp_dict = {k: v for k, v in data.dict().items() if v is not None}
    result = col.update_one({"id": data.id}, {"$set": emp_dict})
    if result.modified_count == 1:
        return {"message": f"Employee {data.name} updated."}
    return {"message": f"error occured while updating employee {data.name}"}


@app.delete("/employee/{id}")
def delete_employee(id: int):
    db = get_db()
    col = db.get_collection("Employee")
    result = col.delete_one({"id": id})
    if result.deleted_count == 1:
        return {"message": "Employee deleted"}
    return {"message": "error occured while deleting employee."}
