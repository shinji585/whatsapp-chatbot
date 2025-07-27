from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from models.ChatBot import ChatBot
from models.ProhibitedWords import ProhibitedWordsError

app = FastAPI()
chatbot = ChatBot()  # Instancia del chatbot

class InputMessage(BaseModel):
    text: str

class OutputMessage(BaseModel):
    response: str

@app.post("/chat", response_model=OutputMessage)
def chat_with_bot(message: InputMessage):
    try:
        clean_msg = chatbot.receive_message(message.text)
        response = chatbot.process_message(clean_msg)
        return OutputMessage(response=response)
    except ProhibitedWordsError as e:
        raise HTTPException(status_code=400, detail=str(e))