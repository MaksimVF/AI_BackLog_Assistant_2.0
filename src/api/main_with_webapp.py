
from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
from src.orchestrator.main_orchestrator import main_orchestrator
from src.bot.telegram_bot import telegram_bot
from src.db.connection import AsyncSessionLocal
from src.db.repository import TaskRepository, TriggerRepository
from src.utils.connection_checker import connection_checker
import logging
import asyncio
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI Backlog Assistant API",
    description="API for managing backlog tasks with AI assistance",
    version="0.1.0"
)

@app.on_event("startup")
async def startup_event():
    """Start background tasks when the API starts"""
    logger.info("Starting API startup tasks...")

    # Check external service connections
    try:
        logger.info("🔌 Checking external service connections...")
        connection_status = await connection_checker.check_all_connections()
        logger.info(f"📊 Connection status: {connection_status}")
    except Exception as e:
        logger.error(f"❌ Failed to check connections: {e}")

    # Start Telegram bot in background mode
    try:
        logger.info("🤖 Starting Telegram bot in background mode...")
        asyncio.create_task(telegram_bot.start_polling_background())
        logger.info("✅ Telegram bot started successfully in background")
    except Exception as e:
        logger.error(f"❌ Failed to start Telegram bot: {e}")
        logger.error("⚠️ Telegram bot will not be available")

class ProcessRequest(BaseModel):
    input_data: str
    metadata: Optional[Dict[str, Any]] = None

class TaskRequest(BaseModel):
    input_data: str
    metadata: Optional[Dict[str, Any]] = None

class TaskResponse(BaseModel):
    task_id: str
    status: str
    result: Dict[str, Any]

class TriggerResponse(BaseModel):
    trigger_id: str
    task_id: str
    reason: str
    timestamp: str

@app.get("/")
async def read_root():
    return {"message": "AI Backlog Assistant API is running"}

@app.get("/health")
async def health_check():
    """Check system health including external connections"""
    try:
        # Check connections
        connection_status = await connection_checker.check_all_connections()

        # Determine overall status
        all_connected = all(status.get("connected", False) for status in connection_status.values())
        status = "healthy" if all_connected else "degraded"

        return {
            "status": status,
            "version": "0.1.0",
            "connections": connection_status
        }

    except Exception as e:
        logger.error(f"❌ Health check failed: {e}")
        return {
            "status": "unhealthy",
            "version": "0.1.0",
            "error": str(e)
        }

@app.post("/tasks", response_model=TaskResponse)
async def create_task(request: TaskRequest):
    """
    Create a new task and process it through the workflow
    """
    try:
        logger.info(f"Creating task: {request.input_data[:50]}...")

        # Process through the workflow
        result = main_orchestrator.process_workflow(
            request.input_data,
            request.metadata
        )

        # Generate a simple task ID
        task_id = f"task_{hash(request.input_data) % 1000000}"

        # Extract classification and prioritization results
        classification = result["level2"]["advanced_classification"]
        prioritization = result["level3"]["prioritization"]

        # Prepare task data for database
        task_data = {
            "task_id": task_id,
            "input_data": request.input_data,
            "task_metadata": request.metadata or {},
            "status": "completed",
            "classification": classification["task_type"],
            "sub_category": classification["sub_category"],
            "domain": classification["metadata"]["domain"],
            "sentiment": classification["metadata"]["sentiment"],
            "confidence": classification["confidence"],
            "risk_score": prioritization["risk_score"],
            "impact_score": prioritization["impact_score"],
            "confidence_score": prioritization["confidence_score"],
            "urgency_score": prioritization["urgency_score"],
            "priority_score": prioritization["priority_score"],
            "priority_level": prioritization["priority_level"],
            "priority_recommendation": prioritization["recommendation"],
            "recommendation": result["level4"].get("recommendation", "No recommendation available")
        }

        # Save to database
        async with AsyncSessionLocal() as db:
            await TaskRepository.create_task(db, task_data)

        logger.info(f"Task {task_id} created and saved successfully")

        return {
            "task_id": task_id,
            "status": "completed",
            "result": result
        }

    except Exception as e:
        logger.error(f"Error creating task: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/triggers", response_model=List[TriggerResponse])
async def get_triggers():
    """
    Get active triggers
    """
    try:
        async with AsyncSessionLocal() as db:
            triggers = await TriggerRepository.list_triggers(db, limit=10)

            formatted_triggers = []
            for trigger in triggers:
                formatted_triggers.append({
                    "trigger_id": trigger.trigger_id,
                    "task_id": trigger.task_id,
                    "reason": trigger.reason,
                    "timestamp": trigger.timestamp.isoformat()
                })

            return formatted_triggers

    except Exception as e:
        logger.error(f"Error getting triggers: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Telegram Bot Endpoints
class TelegramMessageRequest(BaseModel):
    message_text: str
    user_id: str = "unknown"

@app.post("/telegram/message")
async def process_telegram_message(request: TelegramMessageRequest):
    """
    Process a Telegram message through the workflow
    """
    try:
        logger.info(f"Processing Telegram message: {request.message_text[:50]}...")

        result = await telegram_bot.process_telegram_message(
            request.message_text,
            request.user_id
        )

        logger.info(f"Telegram message processed successfully")
        return result

    except Exception as e:
        logger.error(f"Error processing Telegram message: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/telegram/status/{task_id}")
async def get_telegram_task_status(task_id: str):
    """
    Get the status of a Telegram task
    """
    try:
        logger.info(f"Getting status for Telegram task: {task_id}")

        result = await telegram_bot.get_task_status(task_id)

        logger.info(f"Telegram task status retrieved successfully")
        return result

    except Exception as e:
        logger.error(f"Error getting Telegram task status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/telegram/tasks")
async def list_telegram_tasks():
    """
    List recent Telegram tasks
    """
    try:
        logger.info("Listing recent Telegram tasks")

        result = await telegram_bot.list_tasks()

        logger.info(f"Telegram tasks listed successfully")
        return result

    except Exception as e:
        logger.error(f"Error listing Telegram tasks: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/telegram/archive/{task_id}")
async def get_telegram_task_archive(task_id: str):
    """
    Get Telegram task archive details
    """
    try:
        logger.info(f"Getting archive for Telegram task: {task_id}")

        result = await telegram_bot.get_task_archive(task_id)

        logger.info(f"Telegram task archive retrieved successfully")
        return result

    except Exception as e:
        logger.error(f"Error getting Telegram task archive: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/process")
async def process_input(request: ProcessRequest):
    """
    Process input through the entire workflow (legacy endpoint)
    """
    try:
        logger.info(f"Processing input: {request.input_data[:50]}...")

        result = main_orchestrator.process_workflow(
            request.input_data,
            request.metadata
        )

        logger.info(f"Processing completed successfully")
        return result

    except Exception as e:
        logger.error(f"Error processing input: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Webapp API Routes (prefixed with /webapp)
class WebappTask(BaseModel):
    id: str
    description: str
    status: str = "new"
    created_at: str = datetime.utcnow().isoformat()
    recommendation: str = "No recommendation yet"

# In-memory task storage for webapp (for demo purposes)
webapp_tasks = []

@app.get("/webapp/")
async def webapp_root():
    """Webapp root endpoint"""
    return {"message": "AI Backlog Assistant Web App API"}

@app.post("/webapp/tasks", response_model=WebappTask)
async def webapp_create_task(task: WebappTask):
    """Create a new task in webapp"""
    logger.info(f"Creating webapp task: {task.id}")
    webapp_tasks.append(task)
    return task

@app.get("/webapp/tasks", response_model=List[WebappTask])
async def webapp_get_tasks():
    """Get all webapp tasks"""
    return webapp_tasks

@app.get("/webapp/tasks/{task_id}", response_model=WebappTask)
async def webapp_get_task(task_id: str):
    """Get a specific webapp task"""
    task = next((t for t in webapp_tasks if t.id == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.put("/webapp/tasks/{task_id}", response_model=WebappTask)
async def webapp_update_task(task_id: str, update_data: Dict[str, Any]):
    """Update a webapp task"""
    task = next((t for t in webapp_tasks if t.id == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    for key, value in update_data.items():
        if hasattr(task, key):
            setattr(task, key, value)

    return task

@app.get("/webapp/recommendations/{task_id}")
async def webapp_get_recommendation(task_id: str):
    """Get recommendation for a webapp task"""
    task = next((t for t in webapp_tasks if t.id == task_id), None)
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
