#!/bin/bash
pyenv local 3.13.0
python3 -m venv ./venv
source ./venv/bin/activate
pip install --upgrade pip
pip3 install -r requirements.txt