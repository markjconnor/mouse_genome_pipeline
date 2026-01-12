#!/usr/bin/env python3

"""
Create a FASTA file containing only sequences whose IDs appear in
experiment_ids.txt

NO non-standard library imports
"""

FASTA_FILE = "/home/almalinux/UP000000589_10090.fasta"
ID_FILE = "/home/almalinux/coursework/experiment_ids.txt"
OUTPUT_FASTA = "/home/almalinux/coursework/experiment_sequences.fasta"


def load_ids(id_file):
    """Load experiment IDs into a set for fast lookup"""
    with open(id_file) as f:
        return set(line.strip() for line in f if line.strip())


def subset_fasta(fasta_file, ids, output_file):
    """
    Stream through FASTA and write only matching entries.
    Uses O(1) memory per sequence.
    """
    write_entry = False

    with open(fasta_file) as fin, open(output_file, "w") as fout:
        for line in fin:
            if line.startswith(">"):
                # Extract ID (first token after '>')
                seq_id = line[1:].split()[0]

                if seq_id in ids:
                    write_entry = True
                    fout.write(line)
                else:
                    write_entry = False
            else:
                if write_entry:
                    fout.write(line)


def main():
    ids = load_ids(ID_FILE)
    subset_fasta(FASTA_FILE, ids, OUTPUT_FASTA)
    print(f"Created subset FASTA: {OUTPUT_FASTA}")


if __name__ == "__main__":
    main()