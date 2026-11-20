#!/usr/bin/env bash
set -euo pipefail

# ------------------------------------------------------------
# Main workflow runner for test‑in‑termux‑docker.yml
# ------------------------------------------------------------
# Prerequisite: Docker daemon must be running and the image
# termux/termux-docker:aarch64 must be available.

# 1. Ensure Docker is reachable
if ! docker info >/dev/null 2>&1; then
  echo "Docker daemon not reachable – starting it..."
  # Try systemd (requires sudo) or user service
  if command -v sudo >/dev/null 2>&1; then
    sudo systemctl start docker || {
      echo "Failed to start Docker via systemd"; exit 1;
    }
  else
    systemctl --user start docker || {
      echo "Failed to start rootless Docker"; exit 1;
    }
  fi
fi

# 2. Pull the required image (cached for future runs)
 echo "Pulling termux/termux-docker:aarch64..."
 docker pull termux/termux-docker:aarch64 || { echo "Image pull failed"; exit 1; }

# 3. Run the workflow using act (acts like GitHub Actions runner)
#    – it will execute both the Docker job and the native Linux job.
#    Install act beforehand if not present.
if ! command -v act >/dev/null 2>&1; then
  echo "act not found – installing..."
  curl -s https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash
fi

echo "Executing workflow (Docker job)..."
act -j test-in-termux-docker || { echo "Docker job failed"; exit 1; }

echo "Executing workflow (Native Linux job)..."
act -j test-native-linux || { echo "Native job failed"; exit 1; }

# 4. Notify user – replace with your preferred method (email, Slack, etc.)
if [ -x "$(command -v ./notify.sh)" ]; then
  ./notify.sh "Termux Docker workflow completed successfully"
fi

echo "✅ Workflow completed"
