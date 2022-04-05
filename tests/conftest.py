import pytest
import mongomock

@pytest.fixture()
def fake_mongo(monkeypatch):
    db=mongomock.MongoClient()
    def fake_db():
        return db
    
    monkeypatch.setattr('main.get_db', fake_mongo)
    
