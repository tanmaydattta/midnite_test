# midnite_test
Test code for midnite
# Fraud Alert Service

This project implements a Flask-based API to detect suspicious user transactions based on predefined rules.

## Features
- `/event` endpoint receives user transactions
- Rules applied:
  - **1100**: Withdraw > 100
  - **30**: 3 consecutive withdraws
  - **300**: 3 consecutive increasing deposits
  - **123**: Cumulative deposits > 200 in 30 seconds

## Run locally
```bash
pip install -r requirements.txt
python app.py

## Docker
     Docker support for tests and running the api
    - Docker compose up 
    - Docker compose test