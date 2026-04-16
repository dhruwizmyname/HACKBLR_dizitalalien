#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
INSTALL_PYTHON_DEPS=1
INSTALL_GH_EXTENSION=1
ENSURE_QDRANT=1

# Parse arguments
for arg in "$@"; do
  case "$arg" in
    --skip-pip)
      INSTALL_PYTHON_DEPS=0
      ;;
    --skip-gh)
      INSTALL_GH_EXTENSION=0
      ;;
    --skip-qdrant)
      ENSURE_QDRANT=0
      ;;
    *)
      echo "Unknown option: $arg" >&2
      exit 1
      ;;
  esac
done

cd "$ROOT_DIR"

# 1. Check Python Dependencies
if [[ "$INSTALL_PYTHON_DEPS" -eq 1 ]]; then
  echo "Checking Python dependencies..."
  MISSING_DEPS=0
  
  # Read requirements.txt and verify each package silently
  if [[ -f "requirements.txt" ]]; then
    while IFS= read -r line || [[ -n "$line" ]]; do
      # Extract base package name (ignores version numbers and comments)
      pkg_name=$(echo "$line" | grep -v '^#' | grep -Eo '^[a-zA-Z0-9_-]+' || true)
      if [[ -n "$pkg_name" ]]; then
        if ! python3 -m pip show "$pkg_name" >/dev/null 2>&1; then
          echo "Package '$pkg_name' missing."
          MISSING_DEPS=1
          break
        fi
      fi
    done < requirements.txt
  else
    MISSING_DEPS=1
  fi

  if [[ "$MISSING_DEPS" -eq 1 ]]; then
    echo "Installing Python requirements..."
    python3 -m pip install --upgrade pip >/dev/null
    python3 -m pip install -r requirements.txt
  else
    echo "Python dependencies are already up to date."
  fi
fi

# 2. Check GitHub Copilot CLI Extension
if [[ "$INSTALL_GH_EXTENSION" -eq 1 ]] && command -v gh >/dev/null 2>&1; then
  echo "Checking GitHub CLI extension..."
  if ! gh extension list | grep -q 'github/gh-copilot'; then
    echo "Installing GitHub Copilot CLI extension..."
    gh extension install github/gh-copilot
  else
    echo "GitHub Copilot CLI already installed."
  fi
fi

# 3. Docker & Qdrant Configuration
if [[ "$ENSURE_QDRANT" -eq 1 ]] && command -v docker >/dev/null 2>&1; then
  echo "Checking Qdrant container..."
  mkdir -p "$ROOT_DIR/qdrant_storage"

  if ! docker info >/dev/null 2>&1; then
    echo "Docker daemon is not running; skipping Qdrant startup."
  else
    # Check if the hackblr-qdrant container exists
    if docker ps -a --format '{{.Names}}' | grep -q '^hackblr-qdrant$'; then
      # Check if it is actively running
      if [[ "$(docker inspect -f '{{.State.Running}}' hackblr-qdrant)" != "true" ]]; then
        echo "Starting existing Qdrant container..."
        docker start hackblr-qdrant >/dev/null
      else
        echo "Qdrant container is already running."
      fi
    else
      echo "Creating new Qdrant container..."
      docker run -d \
        --name hackblr-qdrant \
        -p 6333:6333 \
        -p 6334:6334 \
        -v "$ROOT_DIR/qdrant_storage:/qdrant/storage:z" \
        qdrant/qdrant >/dev/null
    fi
  fi
fi

echo "Setup complete."
