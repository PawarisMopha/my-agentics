#!/usr/bin/env bash
set -euo pipefail

# ------------------------------------------------------------
# Rootless Docker installation for Termux (Android)
# ------------------------------------------------------------
# This script works inside a Termux environment that has:
#   • A recent Android kernel with unprivileged user namespace support
#   • The termux-repository packages (apt) installed
#   • No sudo/root access (rootless mode)
# ------------------------------------------------------------

# 1. Update package index and install required packages
apt update -y
apt install -y ca-certificates curl gnupg xz-utils uidmap git

# 2. Verify that the kernel allows unprivileged user namespaces
if ! sysctl -a | grep -q "kernel.unprivileged_userns_clone = 1"; then
  echo "Enabling unprivileged user namespaces…"
  if [ -w /proc/sys/kernel/unprivileged_userns_clone ]; then
    echo 1 > /proc/sys/kernel/unprivileged_userns_clone || true
  else
    echo "⚠️  Cannot write to /proc/sys/kernel/unprivileged_userns_clone –
You may need to flash a newer Android ROM or enable the feature via
developer options. Continuing anyway, but Docker may fail."
  fi
fi

# 3. Install Docker binaries (Docker Engine) in $HOME/.docker
DOCKER_VER="24.0.7"
mkdir -p $HOME/.docker
cd $HOME/.docker

# Download static binaries (Linux x86_64 – works on most Android devices via termux’s x86_64 emulation)
curl -fSL "https://download.docker.com/linux/static/stable/x86_64/docker-${DOCKER_VER}.tgz" -o docker.tgz
tar -xzf docker.tgz --strip-components=1
rm docker.tgz

# Add Docker to PATH for this session
export PATH="$HOME/.docker:$PATH"

# 4. Set up rootless mode (uses dockerd-rootless-setuptool.sh)
# The script is part of the Docker package; we just downloaded the binaries.
# Create a dedicated user namespace directory
mkdir -p $HOME/.config/docker

# Initialise rootless configuration (creates systemd user unit files if systemd is present)
 dockerd-rootless-setuptool.sh install

# 5. Start the rootless Docker daemon (user systemd service)
# If your Termux has systemd (via termux-services), you can enable it; otherwise start manually.
if command -v systemctl >/dev/null 2>&1; then
  systemctl --user enable docker
  systemctl --user start docker
else
  # Fallback: launch dockerd in background (store PID)
  echo "Starting dockerd-rootless in background…"
  nohup dockerd-rootless.sh > $HOME/.docker/docker.log 2>&1 &
  echo $! > $HOME/.docker/docker.pid
fi

# 6. Verify installation
if docker info >/dev/null 2>&1; then
  echo "✅ Rootless Docker is up and running. Version:" && docker --version
else
  echo "❌ Docker daemon did not start. Check $HOME/.docker/docker.log for details."
  exit 1
fi

# 7. (Optional) Pull the termux/termux-docker:aarch64 image for later use
# Note: this image is built for ARM64; the rootless daemon runs under the same
# architecture as your device, so the pull will succeed on ARM devices.
# On x86_64 devices you can still pull it thanks to QEMU emulation (see README).
# docker pull termux/termux-docker:aarch64 || true

echo "Rootless Docker setup completed. You can now run Docker commands without sudo."
