from http import client
import json
from urllib import response
from fastapi import FastAPI
from fastapi.testclient import TestClient
from matplotlib.pyplot import get

# app=FastAPI()

from main import app


client = TestClient(app)


def test_home():
    response = client.get("/")
    print(type(response), response)
    assert response.status_code == 200
    assert response.json()["message"] == "Welcome Home!!"


def test_get_employee(mongo_mock):
    response = client.get("/employee/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["name"] == "test_user"
    assert response.json()["email"] == "test_user@gmail.com"
    assert response.json()["profession"] == "tester"
    assert response.json()["level"] == "A1"


emp_data = {
    "id": 123,
    "name": "test_user",
    "email": "test_user@gmail.com",
    "profession": "Tester",
    "level": "A1",
}


def test_create_employee(mongo_mock):
    response = client.post("/employee", data=json.dumps(emp_data))
    assert response.status_code == 200
    assert response.json()["message"] == f"Employee {emp_data.get('name')} created"


updated_emp_data = {"id": 1, "profession": "Senior Tester", "level": "A5"}


def test_update_employee(mongo_mock):
    response = client.put("/employee", data=json.dumps(updated_emp_data))
    assert response.status_code == 200
    assert response.json()["message"] == "Employee updated."


def test_delete_employee(mongo_mock):
    response = client.delete("employee/1")
    assert response.status_code == 200
    assert response.json()["message"] == "Employee deleted"
