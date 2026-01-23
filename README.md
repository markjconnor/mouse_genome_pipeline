# COMP0235 Coursework – Data Pipeline

This repository contains the infrastructure and configuration code for the COMP0235 coursework data pipeline. It uses **Terraform** to provision infrastructure and **Ansible** to configure the host and worker nodes.

---

## Prerequisites

Ensure the following are installed on your **local machine**:

- Terraform
- An SSH key pair

---

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

---

## Host Machine Setup

Run the following commands on the host machine:
```bash
sudo dnf install -y git
git clone GITLAB
```

NOTE: You may require a username and password to access the remote Git repository

---

## Network Configuration
1. Return to your local machine
2. Retrieve the Terraform outputs:
    ```bash
    terraform output
    ```
3. Identify the IP addresses for the host node and worker nodes
4. On the **host machine**, update the `ips.json` file with the correct IP addresses for the host and workers

---

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

---

