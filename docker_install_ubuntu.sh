#!/usr/bin/env bash
set -euo pipefail

# ------------------------------------------------------------
# Docker installation script for Ubuntu/Debian
# - Installs Docker Engine (or rootless Docker if sudo unavailable)
# ------------------------------------------------------------

# Detect if we have sudo privileges
if command -v sudo >/dev/null 2>&1; then
  HAS_SUDO=true
else
  HAS_SUDO=false
fi

install_docker_root() {
  echo "Installing Docker Engine with sudo..."
  sudo apt-get update -y
  sudo apt-get install -y ca-certificates curl gnupg lsb-release
  curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
  echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] \
    https://download.docker.com/linux/ubuntu \
    $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
  sudo apt-get update -y
  sudo apt-get install -y docker-ce docker-ce-cli containerd.io
  echo "Docker Engine installed. Version:" && sudo docker --version
}

install_rootless() {
  echo "Installing rootless Docker (no sudo)..."
  # Install binaries via apt (Docker Engine packages also provide rootless binaries)
  apt-get update -y
  apt-get install -y docker-ce-rootless-extras
  # Run the rootless setup script
  dockerd-rootless-setuptool.sh install
  # Enable systemd user service for rootless Docker
  systemctl --user enable docker
  systemctl --user start docker
  echo "Rootless Docker installed. Version:" && docker --version
}

if $HAS_SUDO; then
  install_docker_root
else
  install_rootless
fi

# Verify Docker daemon is reachable
if ! docker info >/dev/null 2>&1; then
  echo "Docker daemon is not reachable. Please check the service status."
  exit 1
fi

echo "Docker setup completed successfully"
