from secrets import token_hex
from time import sleep
from datetime import datetime, timedelta
from contextlib import contextmanager
from .cfg import Config
from .logger import logger

class Guard:
    def __init__(self, db, name = Config.default_name):
        self._db = db
        self._name = name

    def _acquire(self, slug, duration):
        logger.debug(f"Guard: {self._name} attempting to acquire lock: {slug}.")
        now_dt = datetime.utcnow()
        lock_dt = now_dt + duration
        row = self._db.fetch_one(lambda o: f"""
            INSERT INTO {Config.table} VALUES (
                {o(self._name)},
                {o(slug)},
                {o(lock_dt)}
            ) ON CONFLICT (name, slug) DO UPDATE
                SET lock_dt = {o(lock_dt)}
                WHERE {Config.table}.lock_dt <= {o(now_dt)}
            RETURNING *           
        """)
        acquired = row is not None
        status = "succeeded" if acquired else "failed"
        logger.debug(f"Guard: {self._name} acquisition of lock: {slug} {status}.")
        return acquired

    def _release(self, slug):
        logger.debug(f"Guard: {self._name} releasing lock: {slug}.")
        self._db.execute(lambda o: f"""
            DELETE FROM {Config.table}
            WHERE name = {o(self._name)} 
            AND slug = {o(slug)}
        """)

    @contextmanager
    def scope(self, slug, *, duration = Config.default_duration):
        acquired = self._acquire(slug, duration)
        try:
            yield acquired
        finally:
            if acquired:
                self._release(slug)

    @staticmethod
    def setup(db):
        logger.info("Creating lonny_pg_guard DB tables.")
        db.execute(lambda o: f"""
            CREATE TABLE IF NOT EXISTS {Config.table} (
                name TEXT NOT NULL,
                slug TEXT NOT NULL,
                lock_dt TIMESTAMP NOT NULL,
                PRIMARY KEY(name, slug)
            );
        """)

    @staticmethod
    def destroy_dead_locks(db):
        logger.info("Performing deletion of dead locks across ALL guards.")
        db.execute(lambda o: f"""
            DELETE FROM {Config.table}
            WHERE lock_dt < {o(datetime.utcnow())}
        """)