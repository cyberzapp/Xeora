from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from crew import run_crew_task

load_dotenv()

app = FastAPI(title="Xeora Agent Service")

class TaskRequest(BaseModel):
    task_id: str
    title: str
    description: str

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "xeora-agents"}

@app.post("/trigger")
def trigger_agent_workflow(request: TaskRequest):
    try:
        # In a real app, this should run as a background task to not block the request
        # For demonstration, we'll call a dummy crew runner
        result = run_crew_task(request.title, request.description)
        return {"status": "success", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
