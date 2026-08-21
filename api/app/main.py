import os
import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session

from .db import Base, engine, get_db
from .models import Job
from .queue import publish_job

STORAGE_DIR = os.environ["STORAGE_DIR"]
ALLOWED_EXTENSIONS = {".pdf", ".jpg", ".jpeg", ".png"}


@asynccontextmanager
async def lifespan(app: FastAPI):
    os.makedirs(STORAGE_DIR, exist_ok=True)
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="Invoice Intake API", lifespan=lifespan)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/jobs", status_code=202)
async def create_job(file: UploadFile = File(...), db: Session = Depends(get_db)):
    ext = os.path.splitext(file.filename or "")[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(422, f"Unsupported file type: {ext or '(none)'}")

    job_id = str(uuid.uuid4())
    storage_path = os.path.join(STORAGE_DIR, f"{job_id}{ext}")
    contents = await file.read()
    with open(storage_path, "wb") as f:
        f.write(contents)

    job = Job(id=job_id, filename=file.filename, storage_path=storage_path, status="queued")
    db.add(job)
    db.commit()

    publish_job(job_id)

    return {"job_id": job_id, "status": "queued"}


@app.get("/jobs/{job_id}")
def get_job(job_id: str, db: Session = Depends(get_db)):
    job = db.get(Job, job_id)
    if job is None:
        raise HTTPException(404, "Job not found")
    return job.as_dict()


@app.get("/jobs")
def list_jobs(db: Session = Depends(get_db)):
    jobs = db.query(Job).order_by(Job.created_at.desc()).all()
    return [j.as_dict() for j in jobs]
