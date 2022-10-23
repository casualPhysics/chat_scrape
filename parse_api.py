from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel
from whatsapp_parser import text_to_dictionary


app = FastAPI()


class ChatParser(BaseModel):
    filename: str
    prompter: str
    responder: str
    text: Union[str, None]


@app.put("/parser")
async def parse_data(text_data: ChatParser):
    return text_to_dictionary(prompter=text_data.prompter, responder=text_data.responder, text=text_data.text)
