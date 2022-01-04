from typing import Optional
from fastapi import FastAPI
import uvicorn
from service.delivery_optimization import Database, ModelA, ModelB, ModelData
from pydantic import BaseModel

app = FastAPI()
app.database = Database()
app.models = {"A": ModelA(), "B": ModelB()}

class Query(BaseModel):
    username: Optional[str] = None
    product_name: Optional[str] = None


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
def get_prediction(username: str, query: Query):
    group = app.database.get_user_group(username)
    prediction = app.models[group].get_prediction(query.product_name)
    app.database.save_prediction(group, prediction)
    return prediction


if __name__ == "__main__":
    uvicorn.run(app,
                host="127.0.0.1",
                port=8000
                )
