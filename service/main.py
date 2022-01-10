from typing import Optional
from fastapi import FastAPI, UploadFile, File
import uvicorn
from service.delivery_optimization import Database, Models
from pydantic import BaseModel
import os

app = FastAPI()
# app.path = './database/'
app.database = Database()
app.models = Models(app.database.path)

class Query(BaseModel):
    username: Optional[str] = None
    products: Optional[list] = None
    date: Optional[str] = None


@app.get("/")
def root_view():
    return {"project name": "Delivery Optimization", "Endpoint description": "/docs"}

@app.post("/upload-sessions")
def upload_data(sessions: UploadFile = File(...)):
    with open(app.path + "/sessions.jsonl", mode='ab+') as f:
        f.write(sessions.file.read())
    app.models.update_models()
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
    predictions, week_number = app.models.get_predictions(group, products, date)
    app.database.save_prediction(group, predictions, week_number)
    return predictions


if __name__ == "__main__":
    uvicorn.run(app,
                host="127.0.0.1",
                port=8000
                )
