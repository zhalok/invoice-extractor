import json
import os

import pika

RABBITMQ_URL = os.environ["RABBITMQ_URL"]
QUEUE_NAME = "invoice_jobs"


def get_connection() -> pika.BlockingConnection:
    return pika.BlockingConnection(pika.URLParameters(RABBITMQ_URL))


def _publish(message: dict) -> None:
    connection = get_connection()
    try:
        channel = connection.channel()
        channel.queue_declare(queue=QUEUE_NAME, durable=True)
        channel.basic_publish(
            exchange="",
            routing_key=QUEUE_NAME,
            body=json.dumps(message).encode("utf-8"),
            properties=pika.BasicProperties(delivery_mode=2),  # persistent
        )
    finally:
        connection.close()


def publish_job(job_id: str) -> None:
    """New upload -> run the full extract/hydrate/verify(/register) pipeline."""
    _publish({"type": "process", "job_id": job_id})


def publish_submit(job_id: str, payload_override: dict | None) -> None:
    """Human-approved (or auto_submit) job -> register only."""
    _publish({"type": "submit", "job_id": job_id, "payload_override": payload_override})
