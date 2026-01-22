# COMP0235 Coursework Data Pipeline

## Install and Start

- Configure terraform
- Run `terraform apply`
- Copy ssh key to host -> `scp -i ~/.ssh/<KEY_NAME> ~/.ssh/<KEY_NAME> almalinux@<HOST_IP>:/home/almalinux/.ssh/`
- SSH to host machine -> `ssh -i ~/.ssh/<KEY_NAME> <HOST_IP>`
- Run the following commands on the host:

    - `sudo dnf install -y epel-release`
    - `sudo dnf install -y git`
    - `git clone https://github.com/markjconnor/ds4eng-cw.git`

- Go back to local machine
- Run terraform output
- Find ips for host and worker
- Add correct ips for host and workers in ips.json file on host machine


- To run ansible: 
    - Go to ansible directory `cd ds4eng-cw/ansible/`
    - Run ansible script `ansible-playbook -i generate_inventory.py full.yaml --key-file ~/.ssh/<KEY_NAME>`

