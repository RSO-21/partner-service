from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
import threading
from .grpc_server import serve

from prometheus_fastapi_instrumentator import Instrumentator

from .db import get_db, Base, engine
from .api.partners import router as partners_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Partner Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200",  # Angular dev
        "http://localhost:5173",  # Vite (if used)
    ],
    allow_credentials=True,
    allow_methods=["*"],        # ← IMPORTANT
    allow_headers=["*"],        # ← IMPORTANT (X-Tenant-ID!)
)

Instrumentator().instrument(app).expose(app)

@app.on_event("startup")
def start_grpc_server():
    threading.Thread(
        target=serve,
        daemon=True
    ).start()

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ok", "db": "ok"}
    except Exception as e:
        return {"status": "error", "db": str(e)}


@app.get("/")
def root():
    return {"message": "Partner Service is running"}

app.include_router(partners_router)