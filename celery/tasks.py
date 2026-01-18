from celery import Celery
import subprocess
import tempfile
import os
import textwrap
import glob
import csv

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
            f.write(textwrap.dedent(f">{seq_id}\n{sequence}\n"))

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


        # Read this specific task's output
        results_dir = "/home/almalinux/results"
        pattern = os.path.join(results_dir, f"*{seq_id}*_parse.out")
        matches = glob.glob(pattern)

        if not matches:
            return {
                "seq_id": seq_id,
                "success": False,
                "error": "Result file not found",
            }

        result_path = matches[0]

        rows = []
        with open(result_path, newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                row["seq_id"] = seq_id
                rows.append(row)

        return {
            "seq_id": seq_id,
            "rows": rows,
        }

@app.task
def collect_results(results):
    return results
