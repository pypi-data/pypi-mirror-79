from datetime import datetime, timedelta
from .cfg import Configuration
from .logger import logger

class Scheduler:
    def __init__(self, db, name = Configuration.default_name):
        self._db = db
        self._name = name
        self._scheduled = dict()

    def schedule(self, slug = None, *, interval):
        def wrapper(fn):
            final_slug = ":".join([fn.__module__, fn.__name__]) if slug is None else slug
            logger.info(f"Scheduler: {self._name} has registered an event: {final_slug}.")
            self._scheduled[final_slug] = (fn, interval)
            self._db.execute(lambda o: f"""
                INSERT INTO {Configuration.table} VALUES (
                    DEFAULT,
                    {o(self._name)},
                    {o(final_slug)},
                    NULL
                ) ON CONFLICT (slug, name) DO NOTHING
            """)
            return fn
        return wrapper

    def _advance_query(self, o):
        now_dt = datetime.utcnow()
        filters = list()
        cases = list()
        for slug, data in self._scheduled.items():
            cases.append(f"""
                WHEN name = {o(self._name)} AND slug = {o(slug)}
                THEN {o(now_dt)}
            """)
            filters.append(f"""
                OR name = {o(self._name)} AND slug = {o(slug)} 
                AND (last_run_dt < {o(now_dt - data[1])} 
                OR last_run_dt IS NULL)
            """)
        return f"""
            UPDATE {Configuration.table}
            SET last_run_dt = CASE {" ".join(cases)} ELSE last_run_dt END
            WHERE id = (
                SELECT id FROM {Configuration.table}
                WHERE FALSE {" ".join(filters)}
                FOR UPDATE SKIP LOCKED
                LIMIT 1
            )
            RETURNING *
        """

    def run_next(self):
        row = self._db.fetch_one(self._advance_query)
        if row is None:
            return False
        slug = row["slug"]
        logger.debug(f"Event: {slug} is scheduled to run.")
        if slug in self._scheduled:
            self._scheduled[slug][0]()
        return True

    @staticmethod
    def setup(db):
        db.execute(lambda o: f"""
            CREATE TABLE IF NOT EXISTS {Configuration.table} (
                id SERIAL,
                name TEXT NOT NULL,
                slug TEXT NOT NULL,
                last_run_dt TIMESTAMP NULL,
                PRIMARY KEY (id),
                UNIQUE(name, slug)
            )   
        """)
        db.execute(lambda o: f"""
            CREATE INDEX IF NOT EXISTS {Configuration.table}_name_ix ON
                {Configuration.table}(name);
        """)

    @staticmethod
    def destroy_old_events(db, *, max_age = timedelta(days = 28)):
        cutoff_dt = datetime.utcnow() - max_age
        db.execute(lambda o: f"""
            DELETE FROM {Configuration.table}
            WHERE last_run_dt < {o(cutoff_dt)}
        """)
