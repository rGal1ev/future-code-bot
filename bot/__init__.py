from aiogram import Dispatcher, Bot
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from os import getenv

from aiogram_dialog import setup_dialogs

from .dialogs import main, task

dispatcher = Dispatcher(
    storage=MemoryStorage()
)

dispatcher.include_routers(
    main,
    task
)


async def handle_bot():
    bot = Bot(
        token=getenv("TELEGRAM_KEY"),
        parse_mode=ParseMode.HTML
    )

    setup_dialogs(dispatcher)
    await dispatcher.start_polling(bot)
