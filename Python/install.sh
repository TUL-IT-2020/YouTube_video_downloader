#!/bin/bash
# By Pytel

if [ -f requirements.txt ]; then 
    pip install -r requirements.txt
fi

sudo apt install ffmpeg