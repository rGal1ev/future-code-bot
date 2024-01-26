from asyncio import new_event_loop, set_event_loop
from dotenv import load_dotenv

load_dotenv()

from store import init_tables
from bot import handle_bot


async def main() -> None:
    await init_tables()
    await handle_bot()

if __name__ == "__main__":
    loop = new_event_loop()
    set_event_loop(loop)

    loop.run_until_complete(main())
