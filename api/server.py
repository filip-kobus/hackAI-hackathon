from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .worker import SeleniumWorker

app = FastAPI()
session = SeleniumWorker()
session.open_page()
session.initialize()
print("Session initialized")
session.load_history()

class MessageRequest(BaseModel):
    message: str

@app.post("/send_message")
async def send_message(request: MessageRequest):
    message = request.message
    if not message:
        raise HTTPException(status_code=400, detail="Message is required")
    session.send_message(message)
    response = session.check_for_response(session)
    return {"response": response}

@app.get("/get_history")
async def get_history():
    return {"messages": session.messages}