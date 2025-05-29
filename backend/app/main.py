from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import time
import os

from app.config import settings
from app.db.session import init_db
from app.auth.router import router as auth_router
from app.chat.router import router as chat_router
from app.utils.logger import log_http_request

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(
    title="DocBot API",
    description="Medical Chatbot with Authentication",
    version="1.0.0",
    lifespan=lifespan
)

# Add logging middleware for status codes
@app.middleware("http")
async def log_status_codes(request: Request, call_next):
    start_time = time.time()
    
    # Process the request
    response = await call_next(request)
    
    process_time = round((time.time() - start_time) * 1000)
    
    # Extract details
    status_code = response.status_code
    path = request.url.path
    method = request.method
    
    # Log to file
    if not path.startswith("/static/") and not path == "/health":
        log_http_request(method, path, status_code, process_time, request)
    
    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(chat_router, prefix="/chat", tags=["Chat"])

@app.get("/")
async def root():
    return {"message": "DocBot API is running"}

