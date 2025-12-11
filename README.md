# Partner Service

Partner Service is a microservice responsible for managing business partners
in the FRI Food RSO project.  
It exposes:

- **HTTP REST API** (FastAPI, port 8000)
- **gRPC API** for cross-service communication (port 50051)
- **Metrics endpoint** for Prometheus (`/metrics`)

This service is used by the Offer Service to validate partner information via gRPC.

---

## 🚀 Features

- Create, update, list, and retrieve partners
- gRPC server implementing `GetPartner` RPC
- PostgreSQL database (Azure or local)
- Prometheus-compatible metrics
- Dockerized service

---

## 📦 Project Structure
```
partner-service/
├─ app/
│ ├─ main.py # FastAPI entrypoint
│ ├─ grpc_server.py # gRPC server
│ ├─ api/ # HTTP routes
│ ├─ grpc_generated/ # Generated protobuf Python files
│ ├─ models.py
│ ├─ schemas.py
│ ├─ db.py
│ └─ config.py
├─ Dockerfile
├─ requirements.txt
└─ .env.example
```

---

## ⚙️ Environment Variables

Create `.env` file:

```env
PGHOST=your_postgres_host
PGUSER=your_postgres_user
PGPASSWORD=your_postgres_password
PGPORT=5432
PGDATABASE=partner_service
```
---

## ▶️ Running Locally (without Docker)

### 1. Start gRPC server:
python -m app.grpc_server

### 2. Start FastAPI HTTP server:
uvicorn app.main:app --reload --port 8000

---

## 🐳 Running with Docker

### Build the container:
docker build -t partner-service .

### Run the container (HTTP + gRPC):
docker run --name partner-service --network fri-net --env-file .env -p 8000:8000 -p 50051:50051 partner-service

---

## 🌐 Docker Network Requirement

For gRPC communication between microservices to work inside Docker, a shared Docker network is required.

Create the network once on your machine:

docker network create fri-net

Both partner-service and offer-service must run on this shared network:

docker run --network fri-net ...

---

## 📡 HTTP API Documentation

### When running:
http://localhost:8000/docs

---

## 🛰️ gRPC Endpoint

- Host: partner-service
- Port: 50051
- RPC: GetPartner(GetPartnerRequest) returns PartnerResponse

---

## 📊 Metrics

### Prometheus metrics available at:
 /metrics

---

## 🧪 Health Check

GET /health



