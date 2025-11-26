from celery import Celery

app = Celery('tasks')
app.config_from_object('celeryconfig')


@app.task
def run_pipeline():
    """
    Runs the pipeline script on the worker machine.
    fasta_path must exist on that worker machine.
    """
    cmd = ["python3", "/home/almalinux/pipeline_script.py", "/home/almalinux/UP000000589_10090.fasta"]
    result = subprocess.run(cmd, capture_output=True, text=True)

    return {
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }
