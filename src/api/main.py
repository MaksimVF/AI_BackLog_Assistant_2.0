

from fastapi import FastAPI

app = FastAPI(
    title="AI Backlog Assistant API",
    description="API for managing backlog tasks with AI assistance",
    version="0.1.0"
)


@app.get("/")
async def read_root():
    return {"message": "AI Backlog Assistant API is running"}


@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "0.1.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
