#!/bin/sh

echo "UPDATING IMG-API"

cd "${BASH_SOURCE%/*}"

. .venv/bin/activate

pip3 install -r requirements.txt --upgrade


