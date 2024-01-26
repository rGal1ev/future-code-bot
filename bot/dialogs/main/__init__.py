from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram_dialog import Dialog, DialogManager, StartMode, ShowMode

from ..state import MainWindow
from .windows import main_window

dialog = Dialog(
    main_window,
)

router = Router()
router.include_router(dialog)


@router.message(CommandStart())
async def handle_start_message(_: Message,
                               dialog_manager: DialogManager):
    await dialog_manager.start(
        state=MainWindow.main,
        mode=StartMode.RESET_STACK
    )
