from celery import Celery
import subprocess
import tempfile
import os
import textwrap
import glob
import csv
import shutil
from billiard import current_process

app = Celery('tasks')
app.config_from_object('celeryconfig')

successful_task_count = 0
failed_task_count = 0

def output_successful_task():
    global successful_task_count
    successful_task_count += 1
    datum_name = 'task_count{id="'+str(current_process().index)+'"}'
    with open(f'/home/almalinux/custom_metrics/successful_task_count_{current_process().index}.prom.tmp', 'w', encoding="utf-8") as fh:
        fh.write(f'{datum_name} {successful_task_count}\n')
    shutil.move(f'/home/almalinux/custom_metrics/successful_task_count_{current_process().index}.prom.tmp', f'/home/almalinux/custom_metrics/successful_task_count_{current_process().index}.prom')

def output_failed_task():
    global failed_task_count
    failed_task_count += 1
    datum_name = 'task_count{id="'+str(current_process().index)+'"}'
    with open(f'/home/almalinux/custom_metrics/failed_task_count_{current_process().index}.prom.tmp', 'w', encoding="utf-8") as fh:
        fh.write(f'{datum_name} {failed_task_count}\n')
    shutil.move(f'/home/almalinux/custom_metrics/failed_task_count_{current_process().index}.prom.tmp', f'/home/almalinux/custom_metrics/failed_task_count_{current_process().index}.prom')
    
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
            output_failed_task()
            return {
                "seq_id": seq_id,
                "error": "Result file not found",
            }

        result_path = matches[0]

        rows = []
        with open(result_path, newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                row["seq_id"] = seq_id
                rows.append(row)

        output_successful_task()
        return {
            "seq_id": seq_id,
            "rows": rows,
        }

@app.task
def collect_results(results):
    """
    Callback to collect all results from the chord.
    """
    return results
