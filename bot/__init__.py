from aiogram import Dispatcher, Bot
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from aiogram.fsm.storage.memory import MemoryStorage
from os import getenv
from config import Config
from aiogram_dialog import setup_dialogs
from redis.asyncio import Redis
from .dialogs import main, task, test

dispatcher = None

if Config.is_dev:
    dispatcher = Dispatcher(
        storage=MemoryStorage()
    )

else:
    dispatcher = Dispatcher(
        storage=RedisStorage(Redis(), DefaultKeyBuilder(with_destiny=True))
    )


dispatcher.include_routers(
    main, task, test
)


async def handle_bot():
    bot = Bot(
        token=getenv("TELEGRAM_KEY"),
        parse_mode=ParseMode.HTML
    )

    setup_dialogs(dispatcher)
    await dispatcher.start_polling(bot)
