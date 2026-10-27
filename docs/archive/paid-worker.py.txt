import os

from celery import Celery

app = Celery("simufarm", broker=os.environ.get("REDIS_URL", "redis://localhost:6379/0"))
app.conf.update(task_serializer="json", accept_content=["json"], result_serializer="json")


@app.task(name="simufarm.health")
def health():
    return {"status": "ok", "emulator_launch_enabled": False}


# Emulator creation is deliberately not implemented before P4 and host approval.
