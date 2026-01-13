import sys
import os
from subprocess import Popen, PIPE
from Bio import SeqIO
import shutil
import tempfile

"""
usage: python pipeline_script.py INPUT.fasta  
approx 5min per analysis
"""

PYTHON_BIN = '/home/almalinux/venv/bin/python3'

def run_parser(hhr_file, results_file):
    """
    Run the results_parser.py over the hhr file to produce the output summary
    """
    cmd = [PYTHON_BIN, '/home/almalinux/coursework/results_parser.py', hhr_file, results_file]
    print(f'STEP 4: RUNNING PARSER: {" ".join(cmd)}')
    p = Popen(cmd, stdin=PIPE,stdout=PIPE, stderr=PIPE)
    out, err = p.communicate()
    print(out.decode("utf-8"))

    '''
    print("PARSER STDOUT:\n", out.decode())
    print("PARSER STDERR:\n", err.decode())

    if p.returncode != 0:
        raise RuntimeError(f"Parser failed:\n{err.decode()}")

    if not os.path.exists(results_file):
        raise FileNotFoundError(f"{results_file} not created by results_parser.py")

    return results_file
    '''

def run_hhsearch(a3m_file):
    """
    Run HHSearch to produce the hhr file
    """
    cmd = ['/home/almalinux/hhsearch/bin/hhsearch',
           '-i', a3m_file, '-o', hhr_file, '-cpu', '1', '-d', 
           '/home/almalinux/Data/hhdb/pdb70']
    print(f'STEP 3: RUNNING HHSEARCH: {" ".join(cmd)}')
    p = Popen(cmd, stdin=PIPE,stdout=PIPE, stderr=PIPE)
    out, err = p.communicate()

def read_horiz(tmp_file, horiz_file, a3m_file):
    """
    Parse horiz file and concatenate the information to a new tmp a3m file
    """
    pred = ''
    conf = ''
    print("STEP 2: REWRITING INPUT FILE TO A3M")
    with open(horiz_file) as fh_in:
        for line in fh_in:
            if line.startswith('Conf: '):
                conf += line[6:].rstrip()
            if line.startswith('Pred: '):
                pred += line[6:].rstrip()
    with open(tmp_file) as fh_in:
        contents = fh_in.read()
    with open(a3m_file, "w") as fh_out:
        fh_out.write(f">ss_pred\n{pred}\n>ss_conf\n{conf}\n")
        fh_out.write(contents)

def run_s4pred(input_file, horiz_file):
    """
    Runs the s4pred secondary structure predictor to produce the horiz file
    """
    cmd = [PYTHON_BIN, '/home/almalinux/s4pred/run_model.py',
           '-t', 'horiz', '-T', '1', input_file]
    print(f'STEP 1: RUNNING S4PRED: {" ".join(cmd)}')
    p = Popen(cmd, stdin=PIPE,stdout=PIPE, stderr=PIPE)
    out, err = p.communicate()
    with open(horiz_file, "w") as fh_out:
        fh_out.write(out.decode("utf-8"))
    
    with open(horiz_file, "r") as fh_check:
        print("S4PRED OUTPUT:")
        print(fh_check.read())


    
def read_input(file):
    """
    Function reads a fasta formatted file of protein sequences
    """
    print("READING FASTA FILES")
    sequences = {}
    ids = []
    for record in SeqIO.parse(file, "fasta"):
        sequences[record.id] = record.seq
        ids.append(record.id)
    return(sequences)


if __name__ == "__main__":
    sequences = read_input(sys.argv[1])

    for seq_id, sequence in sequences.items():
        print(f'Now analysing input: {seq_id}')

        if not sequence:
            print(f"WARNING: Sequence for {seq_id} is empty, skipping.")
            continue

        # Create a temporary directory for this sequence
        with tempfile.TemporaryDirectory(prefix=f"job_{seq_id}_") as workdir:
            tmp_file = os.path.join(workdir, "tmp.fas")
            horiz_file = os.path.join(workdir, "tmp.horiz")
            a3m_file = os.path.join(workdir, "tmp.a3m")
            hhr_file = os.path.join(workdir, "tmp.hhr")
            results_file = os.path.join(workdir, "hhr_parse.out")

            with open(tmp_file, "w") as fh_out:
                fh_out.write(f">{seq_id}\n{sequence}\n")

            with open(tmp_file, "r") as fh_check:
                print("tmp file OUTPUT:")
                print(fh_check.read())

            run_s4pred(tmp_file, horiz_file)
            read_horiz(tmp_file, horiz_file, a3m_file)
            run_hhsearch(a3m_file)

            run_parser(hhr_file, results_file)

            if os.path.exists(hhr_file):
                print(f"[DEBUG] tmp.hhr exists: {hhr_file}")
            else:
                print(f"[DEBUG] tmp.hhr NOT found! HHsearch may have failed.")
            
            shutil.move(results_file, f'/home/almalinux/results/{seq_id}_parse.out')

            print(f"Task finished: {seq_id}, output: {seq_id}_parse.out")  