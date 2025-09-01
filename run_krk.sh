#!/bin/bash

# Simple script to run KRK Anti-Shutoff
cd "/Users/angeloantonelli/Documents/Coding Projects"

# Activate virtual environment and run script
source krk_venv/bin/activate
python3 krk_anti_shutoff.py "$@"
