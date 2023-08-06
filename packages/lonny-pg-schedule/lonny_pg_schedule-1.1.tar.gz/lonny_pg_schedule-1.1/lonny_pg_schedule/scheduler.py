from datetime import datetime, timedelta
from .cfg import Config
from .logger import logger

class Scheduler:
    def __init__(self, db, name = Config.default_name):
        self._db = db
        self._name = name
        self._jobs = dict()

    def schedule(self, fn, slug = None, *, interval):
        final_slug = ":".join([fn.__module__, fn.__name__]) if slug is None else slug
        self._jobs[final_slug] = (fn, interval)
        self._db.execute(lambda o: f"""
            INSERT INTO {Config.table} VALUES (
                DEFAULT,
                {o(self._name)},
                {o(final_slug)},
                {o(datetime.utcnow())}
            ) ON CONFLICT (slug, name) DO NOTHING
        """)
        logger.debug(f"Scheduler: {self._name} has registered an event: {final_slug}.")

    def _advance_query(self, o):
        now_dt = datetime.utcnow()
        filters = [o(False)]
        cases = list()
        for slug, (_fn, interval) in self._jobs.items():
            cases.append(f"WHEN slug = {o(slug)} THEN {o(now_dt + interval)}")
            filters.append(f"slug = {o(slug)} AND run_dt < {o(now_dt)}")

        return f"""
            UPDATE {Config.table}
            SET run_dt = CASE {" ".join(cases)} ELSE run_dt END
            WHERE id = (
                SELECT id FROM {Config.table}
                WHERE name = {o(self._name)}
                AND run_dt <= {o(now_dt)}
                AND ({" OR ".join(filters)})
                ORDER BY run_dt
                FOR UPDATE SKIP LOCKED
                LIMIT 1
            )
            RETURNING slug
        """

    def run_next(self):
        while True:
            row = self._db.fetch_one(self._advance_query)
            if row is None:
                return False
            slug, = row
            if slug not in self._jobs:
                logger.warn(f"Scheduler: {self._name} has an orphaned event: {slug}.")
                continue
            logger.debug(f"Scheduler: {self._name} is due to run: {slug}.")
            self._jobs[slug][0]()
            return True

    @staticmethod
    def setup(db):
        logger.info("Creating lonny_pg_schedule DB tables and indices.")
        db.execute(lambda o: f"""
            CREATE TABLE IF NOT EXISTS {Config.table} (
                id SERIAL,
                name TEXT NOT NULL,
                slug TEXT NOT NULL,
                run_dt TIMESTAMP NOT NULL,
                PRIMARY KEY (id)
            )   
        """)
        db.execute(lambda o: f"""
            CREATE UNIQUE INDEX IF NOT EXISTS {Config.table}_name_slug_ix ON
                {Config.table}(name, slug);
        """)
        db.execute(lambda o: f"""
            CREATE INDEX IF NOT EXISTS {Config.table}_name_run_dt_ix ON
                {Config.table}(name, run_dt);
        """)

    @staticmethod
    def destroy_dead_events(db):
        logger.info("Performing deletion of dead events.")
        cutoff_dt = datetime.utcnow() - Config.dead_event_duration
        db.execute(lambda o: f"""
            DELETE FROM {Config.table}
            WHERE run_dt < {o(cutoff_dt)}
        """)