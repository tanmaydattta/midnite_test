# midnite_test
Test code for midnite

[![CI](https://github.com/tanmaydattta/midnite_test/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/tanmaydattta/midnite_test/actions/workflows/tests.yml)

# Unusual Activity Alert Service

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
# Create virtual environment
python -m venv venv
source venv/bin/activate   # on macOS/Linux
venv\Scripts\activate      # on Windows

# Install dependencies
pip install -r requirements.txt

python -m midnite_api.app

## or if you like traditional flask way 

```bash
export FLASK_APP=midnite_api.app
export FLASK_ENV=development
flask run --host=0.0.0.0 --port=5000 --reload

The API should be available at:
http://127.0.0.1:5000/event

```

## just run tests and mypy
Ensure you are in the correct virtualenv and use 
```bash

mypy
and 
pytest

```


## With docker


```bash
     Docker support for tests and running the api
    --- to Build and run API
    - Docker compose up  --build midnite_api
    --- to test and run just the tests 
    - Docker compose run test
    --- to check mypy
    - Docker compose run mypy
```



## Example cURL Request (can be extended to postman)

```bash
curl -XPOST http://127.0.0.1:5000/event -H 'Content-Type: application/json' \
-d '{"type": "deposit", "amount": "42.00", "user_id": 1, "t": 0}'


```
## Expected response format:

```bash
curl -XPOST http://127.0.0.1:5000/event -H 'Content-Type: application/json' \
{
  "alert": false,
  "alert_codes": [],
  "user_id": 1
}

```