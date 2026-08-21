import json
import os
import time

import pika
from sqlalchemy.orm import Session

from db import Base, engine, SessionLocal
from models import Job
import pipeline

RABBITMQ_URL = os.environ["RABBITMQ_URL"]
QUEUE_NAME = "invoice_jobs"


def _set_status(db: Session, job: Job, status: str, **fields) -> None:
    job.status = status
    for key, value in fields.items():
        setattr(job, key, value)
    db.add(job)
    db.commit()


def process_job(job_id: str) -> None:
    db = SessionLocal()
    try:
        job = db.get(Job, job_id)
        if job is None:
            print(f"  ! job {job_id} not found, skipping")
            return

        print(f"  -> processing {job_id} ({job.filename})")

        _set_status(db, job, "extracting")
        extracted = pipeline.extract(job.storage_path, job.filename)
        _set_status(db, job, "hydrating", extracted=extracted)

        draft_payload, hydration_issues = pipeline.hydrate(extracted)
        hydration = {"payload": draft_payload, "issues": hydration_issues}
        _set_status(db, job, "verifying", hydration=hydration)

        verification = pipeline.verify(draft_payload, hydration_issues, db)
        if not verification["ok"]:
            _set_status(db, job, "needs_review", verification=verification)
            print(f"     needs_review: {verification['issues']}")
            return

        _set_status(db, job, "registering", verification=verification)
        result = pipeline.register(verification["payload"])
        final_status = "done" if result["success"] else "failed"
        _set_status(db, job, final_status, registration=result)
        print(f"     {final_status}")

    except Exception as exc:  # noqa: BLE001 - report the failure on the job, don't crash the worker
        db.rollback()
        job = db.get(Job, job_id)
        if job is not None:
            _set_status(db, job, "failed", error=str(exc))
        print(f"     ! unexpected error: {exc}")
    finally:
        db.close()


def wait_for_db() -> None:
    for attempt in range(30):
        try:
            Base.metadata.create_all(bind=engine)
            return
        except Exception:  # noqa: BLE001
            time.sleep(1)
    raise RuntimeError("database not reachable")


def main() -> None:
    wait_for_db()

    connection = None
    for attempt in range(30):
        try:
            connection = pika.BlockingConnection(pika.URLParameters(RABBITMQ_URL))
            break
        except pika.exceptions.AMQPConnectionError:
            time.sleep(1)
    if connection is None:
        raise RuntimeError("rabbitmq not reachable")

    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME, durable=True)
    channel.basic_qos(prefetch_count=1)

    def on_message(ch, method, properties, body):
        payload = json.loads(body)
        process_job(payload["job_id"])
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=on_message)
    print("worker: waiting for jobs...")
    channel.start_consuming()


if __name__ == "__main__":
    main()
