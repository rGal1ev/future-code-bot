from aiogram_dialog import DialogManager
from store.actions import get_modules


async def list_window_data(dialog_manager: DialogManager, **kwargs):
    modules = await get_modules()
    is_module_selected = False

    return {
        "modules": modules,
        "selected_module": dialog_manager.dialog_data.get("selected_module", None),
        "test_answers": dialog_manager.dialog_data.get("test_answers", None),

        "is_module_selected": dialog_manager.dialog_data.get("is_module_selected", is_module_selected)
    }


async def answers_edit_data(dialog_manager: DialogManager, **kwargs):
    return {
        "selected_module": dialog_manager.dialog_data.get("selected_module", None),
        "selected_answer": dialog_manager.dialog_data.get("selected_answer", None),
        "test_answers": dialog_manager.dialog_data.get("test_answers", None),

        "action": dialog_manager.dialog_data.get("action", None),
        "number": dialog_manager.dialog_data.get("number", None),
        "value": dialog_manager.dialog_data.get("value", None),
    }


async def test_preview_data(dialog_manager: DialogManager, **kwargs):
    return {
        "test_answers": dialog_manager.dialog_data.get("test_answers", None),
        "selected_answer": dialog_manager.dialog_data.get("selected_answer", None)
    }
