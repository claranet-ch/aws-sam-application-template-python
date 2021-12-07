#!/usr/bin/env bash

clear

echo ""
echo "Creating Virtual Environment to run tests ..."
echo ""

python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r tests/requirements.txt
