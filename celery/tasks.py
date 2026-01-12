from celery import Celery
import subprocess

app = Celery('tasks')
app.config_from_object('celeryconfig')

@app.task
def run_pipeline_for_sequence(seq_id, sequence):
    """
    Run the pipeline for a single FASTA entry.
    """

    with tempfile.TemporaryDirectory(prefix=f"job_{seq_id}_") as workdir:
        fasta_path = os.path.join(workdir, "input.fasta")

        # Write single-entry FASTA
        with open(fasta_path, "w") as f:
            f.write(textwrap.dedent(f""">{seq_id}{sequence}"""))

        cmd = [
            "/home/almalinux/venv/bin/python3",
            "/home/almalinux/coursework/pipeline_script.py",
            fasta_path,
        ]


        result = subprocess.run(
            cmd,
            cwd=workdir,
            capture_output=True,
            text=True,
        )

        return {
            "seq_id": seq_id,
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
        }