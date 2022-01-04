from fastapi.testclient import TestClient
import pytest
import csv
from service.main import app
from service.delivery_optimization import Database

app.database = Database("/service/tests/rsc/")
client = TestClient(app)

def test_root_view():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"project name": "Delivery Optimization", "Endpoint description": "/docs"}

def test_upload_data():
    response = client.post("/upload-data", json={"id": "13"})
    assert response.status_code == 200
    assert response.json() == {"message": "Data uploaded"}

@pytest.mark.parametrize("username,group", [("Dobromiła", "A"), ("Halina", "A")])
def test_append_user(username, group):
    response = client.post("/new-user", json={"username": username})
    assert response.status_code == 200
    assert response.json() == {"message": f"Username {username} added. Your group is {group}"}

@pytest.mark.parametrize("username", ["Karolina"])
def test_do_not_append_user(username):
    response = client.post("/new-user", json={"username": username})
    assert response.status_code == 200
    assert response.json() == {"message": "Sorry, user with that username exists."}

@pytest.mark.parametrize("username", ["Karolina", "Beata"])
def test_get_prediction(username):
    response = client.get(f"/{username}/prediction", json={"product_name": "mleko"})
    assert response.status_code == 200
    assert response.text == '""'

@pytest.fixture(autouse=True)
def fixture_func():
    filename = app.database.get_path("users.csv")
    with open(filename, mode='w', newline='', encoding='UTF-8') as file:
        writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["Karolina", "A"])
        writer.writerow(["Beata", "A"])
