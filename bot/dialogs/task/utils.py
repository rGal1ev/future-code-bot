from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.common import Whenable


def module_id_getter(module):
    return module.id


def task_id_getter(task):
    return task.id


def task_answer_id_getter(task_answer):
    return task_answer.id


def is_module_not_selected(data: dict, widget: Whenable, manager: DialogManager):
    return not data.get("is_module_selected")


def is_ready_to_generate(data: dict, widget: Whenable, manager: DialogManager):
    return data.get("is_module_selected") and data.get("is_task_selected")


def not_is_ready_to_generate(data: dict, widget: Whenable, manager: DialogManager):
    return not (data.get("is_module_selected") and data.get("is_task_selected"))


def is_task_ready(data: dict, widget: Whenable, manager: DialogManager):
    return data.get("number") and data.get("title") and data.get("min_answers_count")
