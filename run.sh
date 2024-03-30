#!/bin/bash

python -m venv venv
source venv/Scripts/activate #for linux/bash
#.\venv\Scripts\activate #for windows
pip install -r requirements.txt
python main.py