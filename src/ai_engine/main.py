import uuid
import logging

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request
from prometheus_fastapi_instrumentator import Instrumentator

from ai_engine.core.config import settings
from ai_engine.core.logging import setup_logging, request_id_var
from ai_engine.api.routes.chat_routes import router as chat_router

# 0) Logging
setup_logging()
access_logger = logging.getLogger("ai_engine.access")

# 1) App
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=getattr(settings, "APP_VERSION", "0.1.0"),
    description="AI Engine - Tech Support Multi-Agent System",
    contact={"name": "FPT Sendo OJT2026-01 Team", "email": "khoile54642005@gmail.com"},
    license_info={"name": "MIT"},
    docs_url="/docs",
    openapi_url="/openapi.json",
    # lifespan=lifespan_manager, # Temp turning off b/c we are not sure if we need
)

# 2) CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    # allow_origins=[str(o) for o in settings.CORS_ORIGINS] or ["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 3) Routers
API_PREFIX = getattr(settings, "APP_PREFIX", "/api/v1")
app.include_router(chat_router,  prefix=API_PREFIX, tags=["Chat/Agent"])

# 4) /metrics (Prometheus)
Instrumentator().instrument(app).expose(app, endpoint="/metrics", include_in_schema=False)

# 5) Middleware để gán Request ID (Cực quan trọng để debug Agent)
@app.middleware("http")
async def add_request_id(request: Request, call_next):
    req_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    token = request_id_var.set(req_id)
    try:
        response = await call_next(request)
        response.headers["X-Request-ID"] = req_id
        return response
    finally:
        request_id_var.reset(token)

@app.get("/")
async def health_check():
    access_logger.info("Health check")
    return {
        "statusCode": 200,
        "status": "Online",
        "project": settings.PROJECT_NAME,
        "mode": "Orchestra of Agents",
        "message": f"Welcome to {settings.PROJECT_NAME} AI Engine",
    }