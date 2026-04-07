#!/usr/bin/env bash

set -euo pipefail

PYTHON_VERSION="3.11.11"
VENV_DIR="${VENV_DIR:-.venv}"

echo "Setting up marketing-analytics-pipeline..."

if command -v pyenv >/dev/null 2>&1; then
  if ! pyenv versions --bare | grep -qx "${PYTHON_VERSION}"; then
    echo "Installing Python ${PYTHON_VERSION} with pyenv..."
    pyenv install "${PYTHON_VERSION}"
  fi
  pyenv local "${PYTHON_VERSION}"
else
  echo "pyenv not found; assuming a compatible Python ${PYTHON_VERSION} interpreter is already available."
fi

python -m venv "${VENV_DIR}"
source "${VENV_DIR}/bin/activate"

python -m pip install --upgrade pip
pip install -r requirements-dev.txt

if [ ! -f ".env" ] && [ -f ".env.example" ]; then
  echo "No .env file found. Copy .env.example to .env and fill in secrets when needed."
fi

if [ ! -f ".streamlit/secrets.toml" ]; then
  echo "Streamlit secrets not found. Google Sheets sync will stay disabled until you add .streamlit/secrets.toml."
fi

echo "Setup complete."
echo "Activate the environment with: source ${VENV_DIR}/bin/activate"
