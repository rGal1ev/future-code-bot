from aiogram_dialog import DialogManager
from store.actions import get_modules


async def list_window_data(dialog_manager: DialogManager, **kwargs):
    modules = await get_modules()

    is_module_selected = False
    is_task_selected = False

    return {
        "selected_module": dialog_manager.dialog_data.get("selected_module", None),
        "selected_task": dialog_manager.dialog_data.get("selected_task", None),

        "modules": dialog_manager.dialog_data.get("modules", modules),
        "tasks": dialog_manager.dialog_data.get("tasks", []),
        "task_answers": dialog_manager.dialog_data.get("task_answers", []),

        "is_task_selected": dialog_manager.dialog_data.get("is_task_selected", is_task_selected),
        "is_module_selected": dialog_manager.dialog_data.get("is_module_selected", is_module_selected)
    }


async def new_module_data(dialog_manager: DialogManager, **kwargs):
    return {
        "message": dialog_manager.dialog_data.get("message", "")
    }


async def new_task_data(dialog_manager: DialogManager, **kwargs):
    return {
        "action": dialog_manager.dialog_data.get("action", None),

        "number": dialog_manager.dialog_data.get("number", None),
        "title": dialog_manager.dialog_data.get("title", None),
        "min_answers_count": dialog_manager.dialog_data.get("min_answers_count", None)
    }


async def answer_tasks_data(dialog_manager: DialogManager, **kwargs):
    return {
        "tasks": dialog_manager.dialog_data.get("tasks", []),

        "task_answer_action": dialog_manager.dialog_data.get("task_answer_id", None),
        "task_answer_id": dialog_manager.dialog_data.get("task_answer_id", None),
        "task_answers": dialog_manager.dialog_data.get("task_answers", []),
        "selected_task_answer": dialog_manager.dialog_data.get("selected_task_answer", None),

        "value": dialog_manager.dialog_data.get("value", None),
        "number": dialog_manager.dialog_data.get("number", None)
    }


async def solution_preview_data(dialog_manager: DialogManager, **kwargs):
    return {
        "solution": dialog_manager.dialog_data.get("solution", "")
    }
