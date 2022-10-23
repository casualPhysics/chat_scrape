from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


class ChatParser(BaseModel):
    filename: str
    prompter: str
    responder: str
    text: Union[str, None]


@app.put("/items/{item_id}")
async def create_item(item_id: int, item: ChatParser, q: Union[str, None] = None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result
