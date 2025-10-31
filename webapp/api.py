


from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import logging
from datetime import datetime

# Initialize FastAPI app
app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# In-memory task storage (for demo purposes)
tasks = []

class Task(BaseModel):
    id: str
    description: str
    status: str = "new"
    created_at: str = datetime.utcnow().isoformat()
    recommendation: str = "No recommendation yet"

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "AI Backlog Assistant Web App API"}

@app.post("/tasks", response_model=Task)
async def create_task(task: Task):
    """Create a new task"""
    logger.info(f"Creating task: {task.id}")
    tasks.append(task)
    return task

@app.get("/tasks", response_model=List[Task])
async def get_tasks():
    """Get all tasks"""
    return tasks

@app.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: str):
    """Get a specific task"""
    task = next((t for t in tasks if t.id == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: str, update_data: Dict[str, Any]):
    """Update a task"""
    task = next((t for t in tasks if t.id == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    for key, value in update_data.items():
        if hasattr(task, key):
            setattr(task, key, value)

    return task

@app.get("/recommendations/{task_id}")
async def get_recommendation(task_id: str):
    """Get recommendation for a task"""
    task = next((t for t in tasks if t.id == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # In a real implementation, this would call the recommendation system
    return {
        "task_id": task_id,
        "recommendation": "Implement this task in the next sprint",
        "risk_mitigation": {
            "strategies": ["Conduct thorough testing", "Implement in stages"],
            "alternatives": ["Consider alternative approach"]
        },
        "resource_optimization": {
            "team_assignments": {"Backend Team": ["API integration"]},
            "reallocation_suggestions": ["Reallocate resources from lower priority tasks"]
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

