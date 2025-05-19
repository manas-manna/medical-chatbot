import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler
from fastapi import Request

# Set up the logs directory relative to the backend folder
# Get the backend directory path
# backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
# log_dir = os.path.join(backend_dir, "logs")

log_dir = "/app/logs"

# Make sure logs directory exists
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Configure file logging with rotation
file_handler = RotatingFileHandler(
    os.path.join(log_dir, "app.log"),
    maxBytes=10485760,  # 10 MB
    backupCount=5       # Keep 5 backup files
)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(levelname)s - %(message)s'
))

# Create logger
logger = logging.getLogger("docbot-api")
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)

# Optional: Also log to console during development
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(levelname)s - %(message)s'
))
logger.addHandler(console_handler)

def get_client_ip(request: Request) -> str:
    """Extract client IP address from request"""
    if "x-forwarded-for" in request.headers:
        return request.headers["x-forwarded-for"]
    elif request.client:
        return request.client.host
    return "unknown"

def log_auth_event(event_type, username, request):
    """Log authentication events"""
    client_ip = get_client_ip(request)
    user_agent = request.headers.get("user-agent", "unknown")
    logger.info(f"AUTH - {event_type} - User: {username} - IP: {client_ip} - Agent: {user_agent}")

def log_http_request(method, path, status_code, duration_ms, request):
    """Log HTTP request details"""
    client_ip = get_client_ip(request)
    logger.info(f"HTTP - {method} {path} - Status: {status_code} - Time: {duration_ms}ms - IP: {client_ip}")