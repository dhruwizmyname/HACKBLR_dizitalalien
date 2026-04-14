#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
INSTALL_PYTHON_DEPS=1
INSTALL_GH_EXTENSION=1
ENSURE_QDRANT=1

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

if [[ "$INSTALL_PYTHON_DEPS" -eq 1 ]]; then
  python3 -m pip install --upgrade pip
  python3 -m pip install -r requirements.txt
fi

if [[ "$INSTALL_GH_EXTENSION" -eq 1 ]] && command -v gh >/dev/null 2>&1; then
  if ! gh extension list | grep -q 'github/gh-copilot'; then
    gh extension install github/gh-copilot
  fi
fi

if [[ "$ENSURE_QDRANT" -eq 1 ]] && command -v docker >/dev/null 2>&1; then
  mkdir -p "$ROOT_DIR/qdrant_storage"

  if ! docker info >/dev/null 2>&1; then
    echo "Docker is installed but daemon is not available; skipping Qdrant startup."
    exit 0
  fi

  if docker ps -a --format '{{.Names}}' | grep -q '^hackblr-qdrant$'; then
    if [[ "$(docker inspect -f '{{.State.Running}}' hackblr-qdrant)" != "true" ]]; then
      docker start hackblr-qdrant >/dev/null
    fi
  else
    docker run -d \
      --name hackblr-qdrant \
      -p 6333:6333 \
      -p 6334:6334 \
      -v "$ROOT_DIR/qdrant_storage:/qdrant/storage:z" \
      qdrant/qdrant >/dev/null
  fi
fi

echo "Setup complete."
