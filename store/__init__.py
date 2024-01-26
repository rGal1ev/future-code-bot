from aiosqlite import connect
from os import getenv
from .queries import TABLES_INIT_LIST

SQLITE_PATH = getenv("SQLITE_PATH")


async def init_tables():
    async with connect(SQLITE_PATH) as db:
        for TABLE_SQL in TABLES_INIT_LIST:
            await db.execute(TABLE_SQL)
            await db.commit()

