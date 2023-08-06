from .logger import logger
from .cfg import Configuration
import json

class Queue():
    def __init__(self, db, name = Configuration.default_name):
        self._db = db
        self._name = name

    def get(self):
        row = self._db.fetch_one(lambda o: f"""
            DELETE FROM {Configuration.table} 
            WHERE id = (
                SELECT id FROM {Configuration.table}
                WHERE name = {o(self._name)}
                FOR UPDATE SKIP LOCKED
                LIMIT 1
            ) RETURNING *
        """)
        if row is None:
            return None
        payload = row["payload"]
        logger.debug(f"Queue: {self._name} has dequeued message: {json.dumps(payload)}")
        return payload

    def put(self, payload):
        logger.debug(f"Queue: {self._name} enqueued with message: {json.dumps(payload)}.")
        self._db.execute(lambda o: f"""
            INSERT INTO {Configuration.table} VALUES (
                DEFAULT,
                {o(self._name)},
                {o(json.dumps(payload))}
            );
        """)

    @staticmethod
    def setup(db):
        db.execute(lambda o: f"""
            CREATE TABLE IF NOT EXISTS {Configuration.table} (
                id SERIAL,
                name TEXT NOT NULL,
                payload JSONB NOT NULL,
                PRIMARY KEY(id)
            );
        """)
        db.execute(lambda o: f"""
            CREATE INDEX IF NOT EXISTS {Configuration.table}_name_ix
                ON {Configuration.table}(name);
        """)