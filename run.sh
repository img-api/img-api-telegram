#!/bin/bash

cd "${BASH_SOURCE%/*}"

export LC_ALL=C.UTF-8
export LANG=C.UTF-8

. .venv/bin/activate

    echo " "
    echo "------------------------------"
    echo "------------ LAUNCH ----------"
    echo "------------------------------"
    echo " "
    python3 imgapi_start.py

$SHELL
