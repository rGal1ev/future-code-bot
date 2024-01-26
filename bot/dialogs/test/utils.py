from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.common import Whenable


def module_id_getter(module):
    return module.id


def test_id_getter(test):
    return test.id


def not_is_module_selected(data: dict, widget: Whenable, manager: DialogManager):
    return not data.get("is_module_selected")


def is_answer_ready(data: dict, widget: Whenable, manager: DialogManager):
    return data.get("number") and data.get("value")
