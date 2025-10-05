
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
from src.orchestrator.main_orchestrator import main_orchestrator
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI Backlog Assistant API",
    description="API for managing backlog tasks with AI assistance",
    version="0.1.0"
)




class ProcessRequest(BaseModel):
    input_data: str
    metadata: Optional[Dict[str, Any]] = None

@app.get("/")
async def read_root():
    return {"message": "AI Backlog Assistant API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "0.1.0"}

@app.post("/process")
async def process_input(request: ProcessRequest):
    """
    Process input through the entire workflow
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
