#!/usr/bin/env bash

clear

echo ""
echo "Running all tests ..."
echo ""

python3 -m unittest discover -s tests
