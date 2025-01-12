from typing import Union

from pydantic import BaseModel

import os

from fastapi import FastAPI, Request

from dotenv import load_dotenv  

from fastapi import FastAPI

from fastapi.responses import HTMLResponse

from fastapi.staticfiles import StaticFiles

from fastapi.templating import Jinja2Templates

from pymongo import MongoClient

from rich.console import Console  # Import Console from rich for colored output
from rich.text import Text  # Import Text for colored text formatting

from config.db import conn
# Load environment variables from .env file
load_dotenv()


   

app = FastAPI()


# db = conn[os.getenv("DB_NAME")]
# notes_collection = db.notes
# sample_note = {"title": "my title2 ", "desc": "something2"}
# notes_collection.insert_one(sample_note)
# console.print(Text("Sample note inserted successfully.", style="green"))



app.mount("/static", StaticFiles(directory="static"), name="static")
templates=Jinja2Templates(directory="templates")

class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    docs = conn[os.getenv("DB_NAME")].notes.find({})
    newDocs=[]
    for doc in docs:
        newDocs.append({
            "id":str(doc["_id"]),"title":doc["title"],"desc":doc["desc"]
        })
    
    return templates.TemplateResponse(
    "index.html", {"request": request, "newDocs": newDocs}
)


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None): #q is recieved in the query params
    return {"item_id": item_id, "q": q}


@app.get("/fullname")
def rearname(firstname:Union[str,None]=None,lastname:Union[str,None]=None):
    return {"fullname":firstname + " "+ lastname}




@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item): # item is recived in the body
    return {"item_name": item.name, "item_id": item_id}