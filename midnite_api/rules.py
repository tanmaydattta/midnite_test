from decimal import Decimal
from typing import List
from midnite_api.constants import EventTypes, TransactionRuleCodes
from midnite_api.storage import SQLiteEventStore


def evaluate_rules(store: SQLiteEventStore, user_id: int) -> List[int]:
    events = store.get_events(user_id)
    codes: List[int] = []

    if not events:
        return codes

    # Rule 1100: Withdraw > 100
    if events[-1]["type"] == EventTypes.WITHDRAW and events[-1]["amount"] > Decimal("100"):
        codes.append(TransactionRuleCodes.WITHDRAW_OVER_100)

    # Rule 30: 3 consecutive withdraws
    if len(events) >= 3 and all(e["type"] == EventTypes.WITHDRAW for e in events[-3:]):
        codes.append(TransactionRuleCodes.THREE_CONSEC_WITHDRAW)

    # Rule 300: 3 consecutive increasing deposits (ignoring withdraws)
    deposits = [e for e in events if e["type"] == EventTypes.DEPOSIT]
    if len(deposits) >= 3:
        if (
            deposits[-3]["amount"] < deposits[-2]["amount"]
            < deposits[-1]["amount"]
        ):
            codes.append(TransactionRuleCodes.THREE_INCREASING_DEPOSITS)

    # Rule 123: deposits in last 30s > 200
    latest_t = events[-1]["t"]
    deposits_30s = [
        e["amount"] for e in events if e["type"] == EventTypes.DEPOSIT and latest_t - e["t"] <= 30
    ]
    if sum(deposits_30s) > Decimal("200"):
        codes.append(TransactionRuleCodes.ACCUM_DEPOSIT_30S)

    return codes
