from celery import Celery
import json
import os

app = Celery("collector")
app.config_from_object("celeryconfig")


@app.task
def collect_results(results):
    """
    Runs after all pipeline tasks complete.
    """

    output_dir = "/home/almalinux/results"
    os.makedirs(output_dir, exist_ok=True)

    summary_path = os.path.join(output_dir, "summary.json")

    with open(summary_path, "w") as f:
        json.dump(results, f, indent=2)

    return {
        "status": "done",
        "num_tasks": len(results),
        "summary_file": summary_path,
    }