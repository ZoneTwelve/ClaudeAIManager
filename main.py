#!/usr/bin/env python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

from src.claude import ClaudeManager, ClaudeVersions

import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

manager = ClaudeManager(os.environ['SESSION_KEY'])

class SessionRequest(BaseModel):
    message: str
    model: Optional[ClaudeVersions] = ClaudeVersions.opus

class MessageRequest(BaseModel):
    uuid: str
    message: str
    model: Optional[ClaudeVersions] = ""

@app.post("/api/session")
def create_session(request: SessionRequest):
    session = manager.CreateSession(message=request.message, model=request.model)
    return {"session_id": session.uuid}

@app.post("/api/conversation/{uuid}")
def send_message(request: MessageRequest, uuid: str):
    if request.uuid not in manager.instance:
        raise HTTPException(status_code=404, detail="Session not found")

    session = manager.instance[request.session_id]
    response = session.send_message(message=request.message, model=request.model)
    return response

@app.get("/api/message/{uuid}")
def get_message(uuid: str):
    if uuid not in manager.instance:
        raise HTTPException(status_code=404, detail="Session not found")

    session = manager.instance[session_id]
    message = session.get_message()
    return message

@app.delete("/conversation/{uuid}")
def delete_session(uuid: str):
    if uuid not in manager.instance:
        raise HTTPException(status_code=404, detail="Session not found")

    session = manager.instance[session_id]
    session.delete()
    del manager.instance[session_id]
    return {"message": "Session deleted"}
