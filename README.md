# COMP0235 Coursework – Data Pipeline

This repository contains the infrastructure and configuration code for the COMP0235 coursework data pipeline. It uses **Terraform** to provision infrastructure and **Ansible** to configure the host and worker nodes.

---

## Prerequisites

Ensure the following are installed on your **local machine**:

- Terraform
- An SSH key pair

## Infrastructure Setup (Terraform)

1. Configure instance labels and variables in Terraform as required.

2. Provision the infrastructure:
   ```bash
   terraform apply
   ```

3. Copy your SSH key to the host machine:
    ```bash
    scp -i ~/.ssh/<KEY_NAME> ~/.ssh/<KEY_NAME> almalinux@<HOST_IP>:/home/almalinux/.ssh/
    ```

## Host Machine Setup

Install required tools and clone the repository:
```bash
sudo dnf install -y git
sudo dnf install -y 
git clone https://gitlab2.ds4eng.condenser.arc.ucl.ac.uk/ucabmjc/ds4eng-cw.git
```

NOTE: You may require a username and password to access the remote Git repository

## Network Configuration
1. Return to your local machine
2. Retrieve the Terraform outputs:
    ```bash
    terraform output
    ```
3. Identify the IP addresses for the host node and worker nodes
4. On the **host machine**, update the `ips.json` file with the correct IP addresses for the host and workers

## Configuration (Ansible)

1. On the host machine, navigate to the Ansible directory:
    ```bash
    cd ds4eng-cw/ansible/
    ```
2. Run the Ansible playbook
    ```bash
    ansible-playbook -i generate_inventory.py full.yaml --key-file ~/.ssh/<KEY_NAME>
    ```

This will setup the host and workers will all the directories and necessary dependencies.

## Running the Data Pipeline and Viewing Results

Once the infrastructure has been configured with Ansible, the data pipeline can be executed from the host machine.

**Running the Pipeline:**

1. SSH into the host machine
2. Navigate to the Celery directory:
    ```bash
    cd ~/ds4eng-cw/celery
    ```
3. Start the distributed pipeline:
    ```bash
    python3 distribute_worker.py
    ```
The host distributes the computation across the worker nodes. Expected runtime is approximately 12 hours using 4 workers.

**Viewing Results**

- Pipeline results:
    https://website-ucabmjc.comp0235.condenser.arc.ucl.ac.uk/
- Pipeline monitoring:
    https://prometheus-ucabmjc.comp0235.condenser.arc.ucl.ac.uk/


## Testing the Data Pipeline

To test the data pipeline, you can run it with a custom FASTA file.

- Open the `/celery/distribute_work.py` script.
- Locate the `fasta_file` variable, which specifies the path to the input FASTA file.
- Update this path to point to the FASTA file you want to test with.
- Run the pipeline as usual; the updated FASTA file will be used as the input for the test run.