#!/usr/bin/env bash
set -euo pipefail

# Basic bootstrap for a fresh Ubuntu host (run once, manually)
# - installs Docker + Compose plugin
# - installs Terraform
#
# Tested on Ubuntu 22.04/24.04.
#
# NOTE: You may prefer installing Docker via official repo for production.

sudo apt-get update
sudo apt-get install -y ca-certificates curl gnupg lsb-release unzip

# Docker (official repo)
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo   "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu   $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo usermod -aG docker $USER

# Terraform (HashiCorp repo)
curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main"   | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt-get update
sudo apt-get install -y terraform

echo "Done. Log out/in to apply docker group membership."
