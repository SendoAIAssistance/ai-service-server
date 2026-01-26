# Entry point: FastAPI cho AI service
from fastapi import FastAPI
from app.routers import ai_router

app = FastAPI(title="Tech Support Agent")

app.include_router(ai_router.router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Tech Support Agent Service is running"}

if __name__ == "__main__": 
    import uvicorn
    uvicorn.run(app, host = "0.0.0.0", port=8801)