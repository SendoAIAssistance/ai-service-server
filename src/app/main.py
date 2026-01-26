# Entry point: FastAPI cho AI service
from fastapi import FastAPI
from app.routers import ai_router

app = FastAPI(title="Tech Support Agent")

app.include_router(ai_router.router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Tech Support Agent Service is running"}

def start():
    """This function will be called with 'sendo-ai-tech-support-server-wakeup' command"""
    # Import setup server here
    # ========================
    #
    # ========================
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8801, reload=True)

if __name__ == "__main__": 
    start()