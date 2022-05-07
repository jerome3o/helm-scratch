import logging
from typing import List

from pydantic import BaseSettings, Field

from psycopg2 import connect
from psycopg2._psycopg import connection
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from fastapi import FastAPI
from dotenv import load_dotenv

_logger = logging.getLogger(__name__)

load_dotenv("app/.env.dev")


class Settings(BaseSettings):
    host: str = Field(env="DB_HOST")
    user: str = Field(env="DB_USER", default="postgres")
    password: str = Field(env="DB_PASSWORD")
    port: int = Field(env="DB_PORT", default=5432)


settings = Settings()


def get_connection_no_db(settings: Settings = None) -> connection:
    s = settings or Settings()
    return connect(f"user={s.user} password={s.password} host={s.host} port={s.port}")


def get_connection(settings: Settings = None) -> connection:
    s = settings or Settings()
    return connect(f"user={s.user} password={s.password} host={s.host} port={s.port} dbname=helmdb")


def try_create_db(con: connection) -> None:
    try:
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = con.cursor()
        cur.execute("CREATE DATABASE helmdb")
    except Exception as e:
        _logger.exception("Didn't initialise db", e)


def try_create_tables(con: connection):
    try:
        cur = con.cursor()
        cur.execute("""
            CREATE TABLE helmtable (
                value varchar
            )
        """)
        cur.execute("""
            INSERT INTO helmtable
            VALUES ('initial value')
        """)
        con.commit()
    except Exception as e:
        _logger.exception("Didn't initialise tables", e)


try_create_db(con=get_connection_no_db(settings))
try_create_tables(con=get_connection(settings))

app = FastAPI()

@app.get("/")
def index() -> dict:
    return {'hello': 'world'}


@app.get("/set/{value}")
def get_value(value: str) -> str:
    con = get_connection(settings)
    cur = con.cursor()
    cur.execute("""
        INSERT INTO helmtable (value) 
        VALUES (%(value)s)
    """, dict(value=value))
    con.commit()
    return "success"

@app.get("/get/")
def get_value() -> List[str]:
    con = get_connection(settings)
    cur = con.cursor()
    cur.execute("SELECT value FROM helmtable")
    return [v[0] for v in cur.fetchall()]


def main():
    from uvicorn import run
    run(app)

if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)
    main()
