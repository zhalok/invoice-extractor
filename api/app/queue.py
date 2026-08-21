import json
import os

import pika

RABBITMQ_URL = os.environ["RABBITMQ_URL"]
QUEUE_NAME = "invoice_jobs"


def get_connection() -> pika.BlockingConnection:
    return pika.BlockingConnection(pika.URLParameters(RABBITMQ_URL))


def publish_job(job_id: str) -> None:
    connection = get_connection()
    try:
        channel = connection.channel()
        channel.queue_declare(queue=QUEUE_NAME, durable=True)
        channel.basic_publish(
            exchange="",
            routing_key=QUEUE_NAME,
            body=json.dumps({"job_id": job_id}).encode("utf-8"),
            properties=pika.BasicProperties(delivery_mode=2),  # persistent
        )
    finally:
        connection.close()
