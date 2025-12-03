FROM python:3.11-slim

WORKDIR /app

# 1) Copy dependencies and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2) Copy source code
COPY app/ ./app/

# 3) Expose HTTP (8000) + gRPC (50051)
EXPOSE 8000 50051

# 4) Start gRPC server in background + FastAPI (uvicorn) in foreground
CMD ["sh", "-c", "python -m app.grpc_server & uvicorn app.main:app --host 0.0.0.0 --port 8000"]
