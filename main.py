from fastapi import FastAPI
from pydantic import EmailStr


app = FastAPI()

@app.get("/")
def hi():
    return{
        "message":"Hi!"
    }


@app.get("/items/{item_id}")
def get_item_id(item_id: int):
    return {
        "item":{
            "id":item_id
        }
    }
@app.get("/items")
def get_items():
    return [
        "Item1",
        "Item2",
        "Item3",
    ]