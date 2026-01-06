#!/usr/bin/env python3

import sys
from Bio import SeqIO

# Fixed locations on the VM
GENOME_FASTA = "/home/almalinux/UP000000589_10090.fasta"

def read_id_list():
    """
    Reads experiment IDs from the file given on the command line
    """
    with open(sys.argv[1]) as fh:
        return set(line.strip() for line in fh if line.strip())

def subset_fasta(output_fasta="experiment_sequences.fasta"):
    """
    Subsets the genome FASTA using experiment IDs
    """
    ids = read_id_list()
    found = 0

    with open(output_fasta, "w") as out_fh:
        for record in SeqIO.parse(GENOME_FASTA, "fasta"):
            if record.id in ids:
                SeqIO.write(record, out_fh, "fasta")
                found += 1

    print(f"Written {found} sequences to {output_fasta}")

if __name__ == "__main__":

    if len(sys.argv) != 2:
        raise SystemExit(
            "Usage: python subset_fasta.py experiment_ids.txt"
        )

    subset_fasta()
