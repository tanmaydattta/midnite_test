import sqlite3
from decimal import Decimal
from typing import List, Dict, Any, Optional
import threading

class SQLiteEventStore:
    def __init__(self, db_path: str = "events.db") -> None:
        self.db_path = db_path
        self._lock = threading.Lock()
        self._init_db()

    def _init_db(self) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    type TEXT NOT NULL,
                    amount TEXT NOT NULL,
                    t INTEGER NOT NULL
                )
                """
            )
            conn.commit()

    def add_event(self, user_id: int, event_type: str, amount: Decimal, t: int) -> None:
        with self._lock, sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT INTO events (user_id, type, amount, t) VALUES (?, ?, ?, ?)",
                (user_id, event_type, str(amount), t),
            )
            conn.commit()

    def get_events(self, user_id: int) -> List[Dict[str, Any]]:
        with self._lock, sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT type, amount, t FROM events WHERE user_id = ? ORDER BY t ASC",
                (user_id,),
            )
            rows = cursor.fetchall()
            return [
                {"type": row[0], "amount": Decimal(row[1]), "t": int(row[2])}
                for row in rows
            ]

    def clear(self, user_id: Optional[int] = None) -> None:
        """For testing: clear events (all or by user)."""
        with self._lock, sqlite3.connect(self.db_path) as conn:
            if user_id is None:
                conn.execute("DELETE FROM events")
            else:
                conn.execute("DELETE FROM events WHERE user_id = ?", (user_id,))
            conn.commit()
