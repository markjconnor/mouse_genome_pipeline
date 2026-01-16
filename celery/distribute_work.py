from celery import chord
from tasks import run_pipeline_for_sequence, collect_results
import json


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


if __name__ == "__main__":
    #TODO Change this back to experiment_sequences.fasta
    fasta_file = "/home/almalinux/coursework/pipeline_example/test.fa"

    entries = parse_fasta(fasta_file)

    tasks = [
        run_pipeline_for_sequence.s(seq_id, sequence)
        for seq_id, sequence in entries
    ]

    job = chord(tasks)(collect_results.s())

    
    print(f"Submitted {len(tasks)} tasks")
    print(f"Chord ID: {job.id}")

    result = job.get()
    print(result)
    with open("all_results.json", "w") as f:
        json.dump(result, f, indent=2)