from typing import List, Dict, Tuple
from fastapi import FastAPI

# schema and types, their validation
# probably a dataclass behind the scenes
from pydantic import BaseModel, ValidationError
from datetime import date

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = None

class User(BaseModel):
    id: int
    name: str = "John Doe"
    joined: date = None
    friends: List[int] = []

user_data = {
    "id": 4,
    "name": "Mary", 
    "joined": "2019-11-30",
}
my_user: User = User(**user_data)

@app.get("/")
def read_root():
    return {"Hello", "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_price": item.price, "item_id": item_id}


@app.post("/items")
def process_item(item_id: int, item: Item):
    return {"item_name": item.name}