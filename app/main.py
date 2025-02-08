from typing import Union
from pydantic import BaseModel
import os
from fastapi import FastAPI, Request
from dotenv import load_dotenv
from .config.db import conn

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None

@app.get("/notes")
async def get_notes():
    docs = conn[os.getenv("DB_NAME")].notes.find({})
    newDocs = []
    for doc in docs:
        newDocs.append({
            "id": str(doc["_id"]),
            "title": doc["title"],
            "desc": doc["desc"]
        })
    return newDocs

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/fullname")
def rearname(firstname: Union[str, None] = None, lastname: Union[str, None] = None):
    return {"fullname": firstname + " " + lastname}

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}