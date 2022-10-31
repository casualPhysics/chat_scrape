from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel
from parsing.whatsapp import text_to_dictionary


app = FastAPI()


@app.get("/")
def read_root():
    return {"Welcome to": "WhatsApp Parser"}


class ChatParser(BaseModel):
    prompter: str
    responder: str
    text: Union[str, None]


@app.put("/parser")
async def parse_data(text_data: ChatParser):
    return text_to_dictionary(prompt=text_data.prompter, response=text_data.responder, text=text_data.text)
