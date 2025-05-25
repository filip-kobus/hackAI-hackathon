"""
FastAPI server for using Selenium.
"""


from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .worker import SeleniumWorker

app = FastAPI()

def initialize_session():
    global session
    session = SeleniumWorker()
    session.open_page()
    session.initialize()

def restart_session():
    global session
    if session:
        session.kill_session()
    session = SeleniumWorker()
    session.open_page()
    session.initialize()

initialize_session()

class MessageRequest(BaseModel):
    message: str

@app.post("/send_message")
async def send_message(request: MessageRequest):
    try:
        message = request.message
        if not message:
            raise HTTPException(status_code=400, detail="Message is required")
        session.is_chat_window_present()

        session.send_message(message)
        response = session.check_for_response()
        return {"response": response}
    except Exception as e:
        print(f"Error: {e}")
        restart_session()
        raise HTTPException(status_code=500, detail="An error occurred while processing the request")