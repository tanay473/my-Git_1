#!/bin/bash
pip3 install -r requirements.txt
export FLASK_APP=app.py
export FLASK_ENV=production
gunicorn app:app
