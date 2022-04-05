from http import client
from fastapi import FastAPI
from fastapi.testclient import TestClient
# app=FastAPI()

from main import app


client=TestClient(app)

def test_home():
    response=client.get('/')
    print(type(response),response)
    assert response.status_code==200
    assert response.json()['message']=='Welcome Home!!'