from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .worker import SeleniumWorker

app = FastAPI()

def initialize_session():
    global session
    session = SeleniumWorker()
    session.open_page()
    session.initialize()

initialize_session()

class MessageRequest(BaseModel):
    message: str

@app.post("/send_message")
async def send_message(request: MessageRequest):
    message = request.message

    if not session.is_chat_window_present():
        print("Chat window is not present. Reloading session.")
        initialize_session() 

    if not message:
        raise HTTPException(status_code=400, detail="Message is required")
    try:
        session.send_message(message)
        response = session.check_for_response(session)
    except Exception as e:
        print("reinitializing session")
        initialize_session()
        raise HTTPException(status_code=500, detail=f"Error processing message: {str(e)}")
    return {"response": response}