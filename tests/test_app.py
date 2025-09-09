import pytest
from midnite_api.app import app, store

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

@pytest.fixture(autouse=True)
def clear_store():
    # Clear DB before and after each test
    store.clear()
    yield
    store.clear()

def post_event(client, payload):
    return client.post("/event", json=payload)

def test_deposit_over_200_in_30s(client):
    user_id = 1
    post_event(client, {"type": "deposit", "amount": "150.00", "user_id": user_id, "t": 0})
    rv = post_event(client, {"type": "deposit", "amount": "100.00", "user_id": user_id, "t": 10})
    data = rv.get_json()
    assert 123 in data["alert_codes"]

def test_withdraw_over_100(client):
    user_id = 2
    rv = post_event(client, {"type": "withdraw", "amount": "150.00", "user_id": user_id, "t": 0})
    data = rv.get_json()
    assert 1100 in data["alert_codes"]

def test_three_consec_withdraws(client):
    user_id = 3
    post_event(client, {"type": "withdraw", "amount": "10.00", "user_id": user_id, "t": 0})
    post_event(client, {"type": "withdraw", "amount": "20.00", "user_id": user_id, "t": 1})
    rv = post_event(client, {"type": "withdraw", "amount": "30.00", "user_id": user_id, "t": 2})
    data = rv.get_json()
    assert 30 in data["alert_codes"]

def test_three_increasing_deposits(client):
    user_id = 4
    post_event(client, {"type": "deposit", "amount": "10.00", "user_id": user_id, "t": 0})
    post_event(client, {"type": "deposit", "amount": "20.00", "user_id": user_id, "t": 1})
    rv = post_event(client, {"type": "deposit", "amount": "30.00", "user_id": user_id, "t": 2})
    data = rv.get_json()
    assert 300 in data["alert_codes"]