from .logger import logger
from .cfg import Config
from datetime import datetime
from contextlib import contextmanager
import json

class Queue():
    def __init__(self, db, name = Config.default_name):
        self._db = db
        self._name = name

    def consume(self, id):
        self._db.execute(lambda o: f"""
            DELETE FROM {Config.table}
            WHERE id = {o(id)}
        """)
        logger.debug(f"Message: {id} consumed")

    def get(self):
        logger.debug(f"Queue: {self._name} attempting to dequeue message.")
        now_dt = datetime.utcnow()
        row = self._db.fetch_one(lambda o: f"""
            UPDATE {Config.table} 
            SET lock_dt = {o(now_dt)},
            retries = retries - 1
            WHERE id = (
                SELECT id FROM {Config.table}
                WHERE name = {o(self._name)}
                AND (lock_dt IS NULL OR lock_dt < ({o(now_dt)} - retry_seconds * interval '1 second'))
                AND retries >= 0
                ORDER BY lock_dt NULLS FIRST
                FOR UPDATE SKIP LOCKED
                LIMIT 1
            ) RETURNING id, payload
        """)
        if row is None:
            logger.debug(f"Queue: {self._name} is empty and no message can be dequeued.")
            return None, None
        id, payload = row
        logger.debug(f"Queue: {self._name} has dequeued message: {id} with payload: {json.dumps(payload)}")
        return payload, id

    def put(self, payload, *, retries = 0, retry_interval = Config.default_retry_interval):
        id, = self._db.fetch_one(lambda o: f"""
            INSERT INTO {Config.table} VALUES (
                DEFAULT,
                {o(self._name)},
                {o(json.dumps(payload))},
                NULL,
                {o(retries)},
                {o(int(retry_interval.total_seconds()))}
            ) RETURNING id;
        """)
        logger.debug(f"Queue: {self._name} enqueued with message: {id} with payload: {json.dumps(payload)}.")
    
    @contextmanager
    def scope(self):
        payload, id = self.get()
        yield payload, id
        if id is not None:
            self.consume(id)

    @staticmethod
    def destroy_expired_messages(db):
        logger.info("Performing deletion of expired messages across ALL queues.")
        db.execute(lambda o: f"""
            DELETE FROM {Config.table}
            WHERE retries < 0
        """)

    @staticmethod
    def setup(db):
        logger.info("Creating lonny_pg_queue DB tables and indices.")
        db.execute(lambda o: f"""
            CREATE TABLE IF NOT EXISTS {Config.table} (
                id SERIAL,
                name TEXT NOT NULL,
                payload JSONB NOT NULL,
                lock_dt TIMESTAMP NULL,
                retries INTEGER NOT NULL,
                retry_seconds INTEGER NOT NULL,
                PRIMARY KEY(id)
            );
        """)
        db.execute(lambda o: f"""
            CREATE INDEX IF NOT EXISTS {Config.table}_name_ix
                ON {Config.table}(name);
        """)
        db.execute(lambda o: f"""
            CREATE INDEX IF NOT EXISTS {Config.table}_lock_dt_ix
                ON {Config.table}(lock_dt NULLS FIRST);
        """)