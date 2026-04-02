import time
import random
import os
from fastapi import FastAPI, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = FastAPI()

# Xác định tên server từ biến môi trường (Docker set)
SERVER_NAME = os.getenv("SERVER_NAME", "unknown-server")

# Định nghĩa Prometheus Metrics
REQUEST_COUNT = Counter(
    'http_requests_total', 'Total HTTP Requests',
    ['method', 'endpoint', 'server']
)
REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds', 'HTTP request latency',
    ['method', 'endpoint', 'server']
)

@app.get("/")
def read_root():
    REQUEST_COUNT.labels(method='GET', endpoint='/', server=SERVER_NAME).inc()
    return {"message": f"Hello from {SERVER_NAME}", "type": "light"}

@app.get("/light")
async def light_task():
    REQUEST_COUNT.labels(method='GET', endpoint='/light', server=SERVER_NAME).inc()
    # Tác vụ cực nhẹ, trả về ngay
    return {"server": SERVER_NAME, "task": "light", "execution_time": "minimal"}

@app.get("/heavy")
async def heavy_task():
    """Mô phỏng tác vụ nặng tốn CPU hoặc xử lý lâu"""
    start_time = time.time()
    REQUEST_COUNT.labels(method='GET', endpoint='/heavy', server=SERVER_NAME).inc()

   
    count = 0
    for i in range(10_000_000): # Điều chỉnh số này tùy sức mạnh máy test
        count += i

    latency = time.time() - start_time
    REQUEST_LATENCY.labels(method='GET', endpoint='/heavy', server=SERVER_NAME).observe(latency)

    return {
        "server": SERVER_NAME,
        "task": "heavy",
        "result": count,
        "execution_time_seconds": latency
    }

# Endpoint để Prometheus kéo data
@app.get("/metrics")
def metrics():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.get("/health")
def health_check():
    return {"status": "ok"}