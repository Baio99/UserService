from fastapi import Request
import time
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

async def log_requests_middleware(request: Request, call_next):
    """Middleware que registra el tiempo de respuesta de cada petición"""
    start_time = time.time()
    
    logger.info(f"📨 Request: {request.method} {request.url.path}")
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    logger.info(f"⏱️  Response time: {process_time:.4f}s | Status: {response.status_code}")
    
    response.headers["X-Process-Time"] = str(process_time)
    
    return response