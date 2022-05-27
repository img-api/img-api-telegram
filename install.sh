#!/usr/bin/env bash

cd "${BASH_SOURCE%/*}"

sudo apt update
sudo apt install software-properties-common

echo "VIRTUAL ENV INSTALL"

sudo apt-get install python3-venv    # If needed
python3 -m venv .venv
source .venv/bin/activate


