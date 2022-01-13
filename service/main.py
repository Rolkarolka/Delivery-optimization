from typing import Optional
from fastapi import FastAPI, UploadFile, File
from starlette.responses import RedirectResponse
import uvicorn
from service.delivery_optimization import Database, Models
from pydantic import BaseModel

app = FastAPI()
app.path = 'service/database/'
app.database = Database(app.path)
app.models = Models(app.path)

class Body(BaseModel):
    username: Optional[str] = None


@app.get("/")
def root_view():
    return RedirectResponse(url="/docs", status_code=301)

@app.post("/upload-sessions")
def upload_data(sessions: UploadFile = File(...)):
    with open(app.path + "/sessions.jsonl", mode='ab+') as f:
        f.write(sessions.file.read())
    app.models.update_models()
    return {"message": "Data uploaded"}

@app.post("/new-user")
def append_new_user(body: Body):
    try:
        group = app.database.create_new_user(body.username)
        return {"message": f"Username {body.username} added. Your group is {group}"}
    except ValueError as er:
        return {"message": "Sorry, user with that username exists."}

@app.get("/{username}/prediction")
def get_predictions(username: str, products, date=None):
    group = app.database.get_user_group(username)
    if products == "all":
        predictions, week_number = app.models.get_all_predictions(group, date)
    else:
        products = list(map(int, products.split(',')))
        predictions, week_number = app.models.get_predictions(group, products, date)
    app.database.save_prediction(group, predictions, week_number)
    return predictions


if __name__ == "__main__":
    uvicorn.run(app,
                host="127.0.0.1",
                port=8000
                )
