import time
from celery import Celery

app = Celery("devtools_worker")

app.conf.update(
    broker_url="redis://:devtools_redis_password@redis:6379/0",
    result_backend="redis://:devtools_redis_password@redis:6379/1",
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
)


@app.task(name="tasks.process_data")
def process_data(data: str) -> dict:
    """Example task that processes data."""
    time.sleep(2)
    return {
        "status": "processed",
        "original": data,
        "processed_at": time.time(),
    }


@app.task(name="tasks.fetch_url")
def fetch_url(url: str) -> dict:
    """Example task that simulates fetching a URL."""
    time.sleep(1)
    return {
        "status": "fetched",
        "url": url,
        "fetched_at": time.time(),
    }


@app.task(name="tasks.generate_report")
def generate_report(report_id: str, params: dict) -> dict:
    """Example task that generates a report."""
    time.sleep(5)
    return {
        "status": "completed",
        "report_id": report_id,
        "params": params,
        "completed_at": time.time(),
    }


@app.task(name="tasks.batch_process")
def batch_process(items: list) -> dict:
    """Example task that processes a batch of items."""
    results = []
    for item in items:
        time.sleep(0.1)
        results.append({"item": item, "processed": True})

    return {
        "status": "completed",
        "total": len(items),
        "processed": results,
        "completed_at": time.time(),
    }


if __name__ == "__main__":
    app.start()
