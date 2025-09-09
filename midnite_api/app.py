from flask import Flask, request, jsonify
from decimal import Decimal
from typing import Dict, Any
from midnite_api.rules import evaluate_rules
from midnite_api.storage import SQLiteEventStore

app = Flask(__name__)
store = SQLiteEventStore()

@app.route("/event", methods=["POST"])
def event() -> Any:
    payload: Dict[str, Any] = request.get_json(force=True)

    event_type: str = payload["type"]
    amount: Decimal = Decimal(payload["amount"])
    user_id: int = int(payload["user_id"])
    t: int = int(payload["t"])

    store.add_event(user_id, event_type, amount, t)
    alert_codes = evaluate_rules(store, user_id)

    response = {
        "alert": bool(alert_codes),
        "alert_codes": alert_codes,
        "user_id": user_id
    }
    return jsonify(response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
