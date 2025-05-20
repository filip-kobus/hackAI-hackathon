from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .worker import SeleniumWorker

app = FastAPI()

def initialize_session():
    global session
    session = SeleniumWorker()
    session.open_page()
    session.initialize()
    session.load_history()

initialize_session()

class MessageRequest(BaseModel):
    message: str

@app.post("/send_message")
async def send_message(request: MessageRequest):
    message = request.message
    if not message:
        raise HTTPException(status_code=400, detail="Message is required")
    try:
        session.send_message(message)
        response = session.check_for_response(session)
    except Exception as e:
        initialize_session()
        raise HTTPException(status_code=500, detail=f"Error processing message: {str(e)}")
    return {"response": response}

@app.get("/get_history")
async def get_history():
    return {"messages": session.messages}