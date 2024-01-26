from aiogram import Router
from aiogram_dialog import Dialog, DialogManager
from .windows import list_window, answers_edit_window, answer_edit_window, test_preview_window


async def getter(dialog_manager: DialogManager, **kwargs):
    return {
        "is_admin": dialog_manager.dialog_data.get("is_admin", dialog_manager.start_data.get("is_admin"))
    }

dialog = Dialog(
    list_window,
    test_preview_window,

    answers_edit_window,
    answer_edit_window,

    getter=getter
)

router = Router()
router.include_router(dialog)
