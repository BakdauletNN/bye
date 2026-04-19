from fastapi import FastAPI, Query, Body
from typing import Optional
import time


app = FastAPI()


@app.get("/sync/{id}")
def sync(id:int):
    print(f"Started Sync func -> {id} ")
    time.sleep(3)


@app.get("/async/{id}")
def async_f(id:int):
    print(f"Started A   Sync func -> {id} ")
    time.sleep(3)

