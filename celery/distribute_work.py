from celery import chord
from tasks import run_pipeline_for_sequence, collect_results
import json
from statistics import mean
import math
import csv
import shutil


def parse_fasta(path):
    
    entries = []
    with open(path) as f:
        seq_id = None
        seq_lines = []

        for line in f:
            line = line.strip()
            if line.startswith(">"):
                if seq_id:
                    entries.append((seq_id, "".join(seq_lines)))
                seq_id = line[1:].split()[0]
                seq_lines = []
            else:
                seq_lines.append(line)

        if seq_id:
            entries.append((seq_id, "".join(seq_lines)))

    return entries

def safe_float(x):
    try:
        return float(x)
    except (ValueError, TypeError):
        return math.nan


def normalize_results(raw_results):
    records = []

    for r in raw_results:
        if not r.get("rows"):
            continue  # safety check

        row = r["rows"][0]  # exactly one row per protein

        records.append({
            "seq_id": r["seq_id"],                
            "best_hit": row["best_hit"],
            "std": safe_float(row["score_std"]),
            "gmean": safe_float(row["score_gmean"]),
        })

    return records

def write_hits_csv(records, path="/home/almalinux/results/hits_output.csv"):
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["fasta_id", "best_hit_id"])

        for r in records:
            writer.writerow([r["seq_id"], r["best_hit"]])


def compute_profile_stats(records):
    stds = [r["std"] for r in records if not math.isnan(r["std"])]
    gmeans = [r["gmean"] for r in records if not math.isnan(r["gmean"])]

    return {
        "ave_std": mean(stds),
        "ave_gmean": mean(gmeans),
    }

def write_profile_csv(stats, path="/home/almalinux/results/profile_output.csv"):
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["ave_std", "ave_gmean"])
        writer.writerow([stats["ave_std"], stats["ave_gmean"]])


if __name__ == "__main__":
    fasta_file = "/home/almalinux/coursework/experiment_sequences.fasta"

    entries = parse_fasta(fasta_file)

    tasks = [
        run_pipeline_for_sequence.s(seq_id, sequence)
        for seq_id, sequence in entries
    ]

    job = chord(tasks)(collect_results.s())

    
    print(f"Submitted {len(tasks)} tasks")
    print(f"Chord ID: {job.id}")

    result = job.get()

    records = normalize_results(result)

    write_hits_csv(records)

    profile_stats = compute_profile_stats(records)
    write_profile_csv(profile_stats)


    # Move output files to web server directory
    shutil.copy("/home/almalinux/results/hits_output.csv", "/var/www/html/data/hits_output.csv")
    shutil.copy("/home/almalinux/results/profile_output.csv", "/var/www/html/data/profile_output.csv")