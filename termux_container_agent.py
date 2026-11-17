#!/usr/bin/env python3
"""Termux Container Agent
=========================
This script abstracts container execution for a Termux project. It selects the
appropriate runtime based on the host environment:

* **Termux on Android** – uses ``udocker`` (if installed) or ``proot-distro``
  to run the ``termux/termux-docker:aarch64`` image.
* **Linux / Server / CI** – uses Docker (or Podman) directly. The ``entrypoint_root.sh``
  script bundled with the image is used when root privileges are required. The
  ``--security-opt seccomp=unconfined`` flag is added automatically when ``root``
  mode is requested.

The agent provides a minimal API:

```python
run_cmd(command: str, *, root: bool = False) -> subprocess.CompletedProcess
```

* ``command`` – the command string to execute *inside* the container.
* ``root`` – when ``True`` the container starts with the ``entrypoint_root.sh``
  entry‑point (provides ``root`` inside the container) and the ``seccomp``
  security option is disabled.

The implementation keeps things quiet – it only prints the container's STDOUT
and STDERR and returns the ``CompletedProcess`` object for further inspection.
"""

import os
import subprocess
import sys
from pathlib import Path
from typing import List

# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def _is_termux_android() -> bool:
    """Detect if we are running inside Termux on Android.

    Termux sets the ``PREFIX`` environment variable (e.g. ``/data/data/com.termux/files/usr``)
    and Android devices expose ``ANDROID_ROOT``/``ANDROID_DATA``. If both are present we
    assume a Termux environment.
    """
    return bool(os.getenv("PREFIX")) and bool(os.getenv("ANDROID_ROOT"))


def _has_executable(name: str) -> bool:
    """Check whether *name* exists in ``PATH`` and is executable."""
    return any(
        os.access(os.path.join(p, name), os.X_OK) for p in os.getenv("PATH", "").split(":")
    )


def _run_subprocess(args: List[str], capture_output: bool = True) -> subprocess.CompletedProcess:
    """Run *args* via ``subprocess.run`` with sensible defaults.

    ``capture_output`` mirrors ``subprocess.run(..., capture_output=True)`` but also
    forwards ``stderr`` to the console when not capturing – helpful for debugging.
    """
    try:
        return subprocess.run(
            args,
            check=False,
            text=True,
            capture_output=capture_output,
        )
    except FileNotFoundError as e:
        print(f"[ERROR] Command not found: {args[0]}", file=sys.stderr)
        raise e

# ---------------------------------------------------------------------------
# Container wrapper
# ---------------------------------------------------------------------------
class TermuxContainerAgent:
    """High‑level wrapper that abstracts away the underlying container engine.

    The public method ``run_cmd`` executes a *single* command inside the container.
    For more complex workflows you can call ``run_cmd`` repeatedly – each call
    creates a short‑lived container that is removed after execution (``--rm``).
    """

    IMAGE = "termux/termux-docker:aarch64"
    ENTRYPOINT_ROOT = "/entrypoint_root.sh"

    def __init__(self):
        self.is_termux = _is_termux_android()
        if self.is_termux:
            self.engine = self._detect_termux_engine()
            print(f"[INFO] Detected Termux environment – using engine: {self.engine}")
        else:
            self.engine = self._detect_linux_engine()
            print(f"[INFO] Detected Linux/CI environment – using engine: {self.engine}")

    # ---------------------------------------------------------------------
    # Engine detection helpers
    # ---------------------------------------------------------------------
    def _detect_termux_engine(self) -> str:
        """Prefer ``udocker``; fall back to ``proot-distro``.

        ``udocker`` can pull and run Docker images without a daemon. ``proot-distro``
        ships with Termux and can launch a distribution from a rootfs.
        """
        if _has_executable("udocker"):
            return "udocker"
        if _has_executable("proot-distro"):
            return "proot-distro"
        raise RuntimeError(
            "Neither 'udocker' nor 'proot-distro' is available in Termux. Install one of them."
        )

    def _detect_linux_engine(self) -> str:
        """Prefer Docker; fall back to Podman if Docker is missing."""
        if _has_executable("docker"):
            return "docker"
        if _has_executable("podman"):
            return "podman"
        raise RuntimeError(
            "Neither 'docker' nor 'podman' is installed on this system. Install one to use the agent."
        )

    # ---------------------------------------------------------------------
    # Public API
    # ---------------------------------------------------------------------
    def run_cmd(self, command: str, *, root: bool = False) -> subprocess.CompletedProcess:
        """Run *command* inside the chosen container.

        Parameters
        ----------
        command: str
            The shell command to execute **inside** the container.
        root: bool, optional
            When ``True`` the container starts with ``entrypoint_root.sh`` and the
            ``seccomp=unconfined`` security option, granting root privileges inside
            the container.
        """
        if self.engine in ("docker", "podman"):
            return self._run_with_docker_like(command, root=root)
        if self.engine == "udocker":
            return self._run_with_udocker(command, root=root)
        if self.engine == "proot-distro":
            return self._run_with_proot_distro(command, root=root)
        raise RuntimeError(f"Unsupported engine: {self.engine}")

    # ---------------------------------------------------------------------
    # Engine‑specific implementations
    # ---------------------------------------------------------------------
    def _base_docker_cmd(self, root: bool) -> List[str]:
        cmd = [self.engine, "run", "--rm", "-i"]
        if root:
            cmd += ["--entrypoint", self.ENTRYPOINT_ROOT, "--security-opt", "seccomp=unconfined"]
        cmd += [self.IMAGE]
        return cmd

    def _run_with_docker_like(self, command: str, *, root: bool) -> subprocess.CompletedProcess:
        full_cmd = self._base_docker_cmd(root) + ["/bin/sh", "-c", command]
        print(f"[DEBUG] Executing: {' '.join(full_cmd)}")
        return _run_subprocess(full_cmd)

    def _run_with_udocker(self, command: str, *, root: bool) -> subprocess.CompletedProcess:
        # Pull the image if necessary
        _run_subprocess(["udocker", "pull", self.IMAGE], capture_output=False)
        container_name = "termux_container_agent"
        args = ["udocker", "run", "--name", container_name]
        if root:
            args += ["--entrypoint", self.ENTRYPOINT_ROOT]
        args += [self.IMAGE, "/bin/sh", "-c", command]
        print(f"[DEBUG] Executing udocker: {' '.join(args)}")
        result = _run_subprocess(args)
        # Cleanup – udocker does not have an automatic --rm flag.
        _run_subprocess(["udocker", "rm", container_name], capture_output=False)
        return result

    def _run_with_proot_distro(self, command: str, *, root: bool) -> subprocess.CompletedProcess:
        # Assume a distro named 'termux' is already installed via proot-distro.
        distro = "termux"
        exec_cmd = ["proot-distro", "login", distro, "--", "/bin/sh", "-c", command]
        print(f"[DEBUG] Executing proot-distro: {' '.join(exec_cmd)}")
        return _run_subprocess(exec_cmd)

# ---------------------------------------------------------------------------
# Simple CLI for manual testing
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: termux_container_agent.py '<command>' [--root]", file=sys.stderr)
        sys.exit(1)
    cmd = sys.argv[1]
    root_flag = "--root" in sys.argv
    agent = TermuxContainerAgent()
    result = agent.run_cmd(cmd, root=root_flag)
    print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    sys.exit(result.returncode)
