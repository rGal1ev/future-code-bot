from aiogram import Router
from aiogram_dialog import Dialog, DialogManager
from .windows import (
    list_window, task_answers_edit_window,
    solution_preview_window
)
from ..state import TaskWindow
from ...widgets.alert import AlertWindow
from ...widgets.form import FormWindow


async def getter(dialog_manager: DialogManager, **kwargs):
    return {
        "is_admin": dialog_manager.dialog_data.get("is_admin", dialog_manager.start_data.get("is_admin"))
    }

dialog = Dialog(
    list_window,

    solution_preview_window,
    task_answers_edit_window,

    AlertWindow(TaskWindow.alert),
    FormWindow(TaskWindow.form),

    getter=getter
)

router = Router()
router.include_routers(dialog)
