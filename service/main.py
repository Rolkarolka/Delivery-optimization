from typing import Optional
from fastapi import FastAPI
import uvicorn
from service.delivery_optimization import Database, Models, ModelData
from pydantic import BaseModel

app = FastAPI()
app.database = Database()
app.models = Models()

class Query(BaseModel):
    username: Optional[str] = None
    products: Optional[list] = None
    date: Optional[str] = None


@app.get("/")
def root_view():
    return {"project name": "Delivery Optimization", "Endpoint description": "/docs"}

@app.post("/upload-data")
def upload_data(data: ModelData):
    for model in app.models.values():
        model.update_model(data)
    return {"message": "Data uploaded"}

@app.post("/new-user")
def append_new_user(query: Query):
    try:
        group = app.database.create_new_user(query.username)
        return {"message": f"Username {query.username} added. Your group is {group}"}
    except ValueError as er:
        return {"message": "Sorry, user with that username exists."}

@app.get("/{username}/prediction")
def get_predictions(username: str, products, date=None):
    products = list(map(int, products.split(',')))
    group = app.database.get_user_group(username)
    predictions = app.models.get_predictions(group, products, date)
    # app.database.save_prediction(group, predictions)
    return predictions


if __name__ == "__main__":
    # app.models.get_predictions("A", [1114], 126)
    uvicorn.run(app,
                host="127.0.0.1",
                port=8000
                )
