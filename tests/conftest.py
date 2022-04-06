import pytest
import mongomock

from main import Employee


@pytest.fixture()
def mongo_mock(monkeypatch):
    client = mongomock.MongoClient()
    db = client.get_database("EmployeeDB")
    col = db.get_collection("Employee")
    emp_data: Employee = {
        "id": 1,
        "name": "test_user",
        "email": "test_user@gmail.com",
        "profession": "tester",
        "level": "A1",
    }

    col.insert_one(emp_data)

    def fake_db():
        return db

    monkeypatch.setattr("main.get_db", fake_db)
