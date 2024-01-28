from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import ManagedTextInput
from aiogram_dialog.widgets.kbd import Button
from ..state import TaskWindow
from ...helpers import generate_task_solution
from ...widgets.form import trigger_form

from store.actions import (
    get_tasks, get_module_by_id, get_task_by_id, add_module,
    delete_module, get_modules, add_task, delete_task, get_task_answers, get_task_answer_by_id,
    update_task_answer_by_id, add_task_answer, delete_task_answer_by_id, update_module, update_task
)


async def handle_module_select(callback: CallbackQuery, widget: any,
                               manager: DialogManager, item_id: str):
    module_id = int(item_id)
    tasks = await get_tasks(module_id)
    module = await get_module_by_id(module_id)

    manager.dialog_data.update({
        "tasks": tasks,
        "is_module_selected": True,
        "selected_module": module
    })


async def handle_module_deselect(callback: CallbackQuery, button: Button,
                                 manager: DialogManager):
    manager.dialog_data.update({
        "tasks": [],
        "is_module_selected": False
    })


async def handle_task_select(callback: CallbackQuery, widget: any,
                             manager: DialogManager, item_id: str):
    task_id = int(item_id)

    task = await get_task_by_id(task_id)
    task_answers = await get_task_answers(task_id)

    manager.dialog_data.update({
        "is_task_selected": True,

        "selected_task": task,
        "task_answers": task_answers
    })


async def handle_task_deselect(callback: CallbackQuery, button: Button,
                               manager: DialogManager):
    manager.dialog_data.update({
        "selected_task": None,
        "is_task_selected": False
    })


async def handle_module_create(callback: CallbackQuery, button: Button,
                               manager: DialogManager, data: dict):
    new_module_id = await add_module(data["number"], data["title"])
    modules = await get_modules()
    selected_module = await get_module_by_id(new_module_id)

    manager.dialog_data.update({
        "selected_module": selected_module,
        "modules": modules,
        "is_module_selected": True
    })

    await manager.switch_to(
        state=TaskWindow.list
    )


async def handle_module_delete(callback: CallbackQuery, button: Button,
                               manager: DialogManager):
    selected_module = manager.dialog_data.get("selected_module")
    await delete_module(selected_module["id"])
    modules = await get_modules()

    manager.dialog_data.update({
        "modules": modules,
        "selected_module": None,
        "is_module_selected": False
    })

    await manager.switch_to(
        TaskWindow.list
    )


async def handle_task_action_change(callback: CallbackQuery, button: Button,
                                    manager: DialogManager):
    manager.dialog_data.update({
        "action": button.widget_id
    })

    await callback.answer("Отправьте значение")


async def handle_task_info_input(message: Message,
                                 manager_input: ManagedTextInput,
                                 dialog_manager: DialogManager,
                                 text: str):
    action = dialog_manager.dialog_data.get("action")

    if action is None:
        action = "number"

    dialog_manager.dialog_data.update({
        action: text
    })


async def handle_task_create(callback: CallbackQuery, button: Button,
                             manager: DialogManager, data):
    module_id = manager.dialog_data.get("selected_module")["id"]

    new_task_id = await add_task(title=data.get("title"),
                   number=int(data.get("number")),
                   module_id=module_id,
                   min_answers_count=int(data.get("min_answers_count")))

    tasks = await get_tasks(module_id=module_id)
    selected_task = await get_task_by_id(new_task_id)

    manager.dialog_data.update({
        "selected_task": selected_task,
        "is_task_selected": True
    })

    await manager.switch_to(TaskWindow.list)

    manager.dialog_data.update({
        "tasks": tasks
    })


async def handle_task_delete(callback: CallbackQuery, button: Button,
                             manager: DialogManager):
    task_id = manager.dialog_data.get("selected_task")["id"]

    await delete_task(task_id=task_id)
    tasks = await get_tasks(manager.dialog_data.get("selected_module")["id"])

    manager.dialog_data.update({
        "selected_task": None,
        "is_task_selected": False,
        "tasks": tasks
    })

    await manager.switch_to(
        state=TaskWindow.list
    )


async def handle_task_answer_select(callback: CallbackQuery, widget: any,
                                    manager: DialogManager, item_id: str):
    task_answer_id = int(item_id)
    selected_task_answer = await get_task_answer_by_id(task_answer_id)

    manager.dialog_data.update({
        "task_answer_id": item_id,

        "selected_task_answer": selected_task_answer,
        "number": selected_task_answer["number"],
        "value": selected_task_answer["value"]
    })

    await trigger_form(
        title="✏️ Редактирование ответа",
        manager=manager,
        model={
            "number": {
                "title": "Номер",
                "emoji": "❶",
                "required": True,
                "default": selected_task_answer["number"],
            },
            "value": {
                "title": "Ответ",
                "emoji": "❷",
                "type": "code",
                "required": True,
                "default": selected_task_answer["value"]
            }
        },

        show_delete_button=True,
        handler=handle_task_answer_form_saving,
        delete_handler=handle_task_answer_delete,
        state=TaskWindow.form
    )


async def handle_task_answer_form_saving(callback: CallbackQuery, button: Button,
                                         manager: DialogManager, data: dict):
    task_id = manager.dialog_data.get("selected_task")["id"]
    task_answer_id = manager.dialog_data.get("task_answer_id")

    await update_task_answer_by_id(task_answer_id, data.get("number"), data.get("value"))
    task_answers = await get_task_answers(task_id)
    manager.dialog_data.update({
        "task_answers": task_answers
    })

    await manager.switch_to(TaskWindow.task_answers_edit)


async def handle_task_answer_form_creation(callback: CallbackQuery, button: Button,
                                           manager: DialogManager, data: dict):
    task_id = manager.dialog_data.get("selected_task")["id"]

    await add_task_answer(task_id, data.get("number"), data.get("value"))
    task_answers = await get_task_answers(task_id)
    manager.dialog_data.update({
        "task_answers": task_answers
    })

    await manager.switch_to(
        state=TaskWindow.task_answers_edit
    )


async def handle_task_answer_delete(callback: CallbackQuery, button: Button,
                                    manager: DialogManager):
    task_id = manager.dialog_data.get("selected_task")["id"]
    task_answer_id = manager.dialog_data.get("task_answer_id")

    await delete_task_answer_by_id(task_answer_id)
    task_answers = await get_task_answers(task_id)

    manager.dialog_data.update({
        "task_answers": task_answers
    })

    await manager.switch_to(
        state=TaskWindow.task_answers_edit
    )

    manager.dialog_data.update({
        "task_answer_id": None,
        "selected_task_answer": None,

        "number": None,
        "value": None
    })


async def handle_task_solution_generate(callback: CallbackQuery, button: Button,
                                        manager: DialogManager):
    task = manager.dialog_data.get("selected_task")
    task_answers = manager.dialog_data.get("task_answers")
    solution = generate_task_solution(task, task_answers)

    manager.dialog_data.update({
        "solution": solution
    })
    await manager.switch_to(
        state=TaskWindow.preview
    )


async def handle_module_form_saving(callback: CallbackQuery, button: Button,
                                    manager: DialogManager, data: dict):
    module_id = manager.dialog_data.get("selected_module")["id"]
    await update_module(module_id, data["title"], data["number"])

    modules = await get_modules()
    selected_module = await get_module_by_id(module_id)

    manager.dialog_data.update({
        "modules": modules,
        "selected_module": selected_module
    })

    await manager.switch_to(TaskWindow.list)


async def handle_module_edit(callback: CallbackQuery, button: Button,
                             manager: DialogManager):
    selected_module = manager.dialog_data.get("selected_module")

    await trigger_form(
        title="✏️ Редактирование модуля",
        manager=manager,
        model={
            "number": {
                "title": "Номер",
                "emoji": "❶",
                "required": True,
                "default": selected_module["number"],
            },
            "title": {
                "title": "Название",
                "emoji": "❷",
                "required": True,
                "default": selected_module["title"]
            }
        },

        show_delete_button=True,
        handler=handle_module_form_saving,
        delete_handler=handle_module_delete,
        state=TaskWindow.form
    )


async def handle_task_form_saving(callback: CallbackQuery, button: Button,
                                    manager: DialogManager, data: dict):
    task_id = manager.dialog_data.get("selected_task")["id"]
    module_id = manager.dialog_data.get("selected_module")["id"]

    await update_task(task_id, data["title"], data["number"], data["min_answers_count"], module_id)

    tasks = await get_tasks(module_id)
    selected_task = await get_task_by_id(task_id)

    manager.dialog_data.update({
        "tasks": tasks,
        "selected_task": selected_task
    })

    await manager.switch_to(TaskWindow.list)


async def handle_task_form_delete(callback: CallbackQuery, button: Button,
                                  manager: DialogManager):
    task_id = manager.dialog_data.get("selected_task")["id"]
    module_id = manager.dialog_data.get("selected_module")["id"]

    await delete_task(task_id)
    tasks = await get_tasks(module_id)

    manager.dialog_data.update({
        "selected_task": None,
        "tasks": tasks,
        "is_task_selected": False
    })

    await manager.switch_to(TaskWindow.list)


async def handle_task_edit(callback: CallbackQuery, button: Button,
                           manager: DialogManager):
    selected_task = manager.dialog_data.get("selected_task")

    await trigger_form(
        title="✏️ Редактирование модуля",
        manager=manager,
        model={
            "number": {
                "title": "Номер",
                "emoji": "❶",
                "required": True,
                "default": selected_task['number'],
            },
            "title": {
                "title": "Название",
                "emoji": "❷",
                "required": True,
                "default": selected_task['title']
            },
            "min_answers_count": {
                "title": "Минимальное кол-во ответов",
                "emoji": "❸",
                "required": True,
                "default": selected_task['min_answers_count']
            }
        },

        show_delete_button=True,
        handler=handle_task_form_saving,
        delete_handler=handle_task_form_delete,
        state=TaskWindow.form
    )
