import os
import logging
from typing import List

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

from .models import Base, Submission

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=LOG_LEVEL, format="%(asctime)s %(levelname)s %(name)s - %(message)s")
logger = logging.getLogger("app")

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")

# SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    future=True,
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="DevOps Task App", version="1.0.0")

# Templates/static
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Prometheus metrics
REQUEST_COUNT = Counter("http_requests_total", "Total HTTP requests", ["method", "path", "status"])
REQUEST_LATENCY = Histogram("http_request_duration_seconds", "HTTP request latency", ["method", "path"])

@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    path = request.url.path
    method = request.method
    with REQUEST_LATENCY.labels(method=method, path=path).time():
        response = await call_next(request)
    REQUEST_COUNT.labels(method=method, path=path, status=str(response.status_code)).inc()
    return response

@app.get("/healthz", response_class=PlainTextResponse)
def healthz():
    return "ok"

@app.get("/metrics")
def metrics():
    return PlainTextResponse(generate_latest().decode("utf-8"), media_type=CONTENT_TYPE_LATEST)

def get_last_submissions(db, limit: int = 5) -> List[Submission]:
    return db.query(Submission).order_by(Submission.created_at.desc()).limit(limit).all()

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    with SessionLocal() as db:
        submissions = get_last_submissions(db, 5)
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "submissions": submissions},
        )

@app.post("/submit")
def submit(text: str = Form(...)):
    text = (text or "").strip()
    if not text:
        return RedirectResponse(url="/", status_code=303)

    with SessionLocal() as db:
        sub = Submission(text=text)
        db.add(sub)
        db.commit()
        logger.info("New submission saved: %s", text[:200])

    return RedirectResponse(url="/", status_code=303)
