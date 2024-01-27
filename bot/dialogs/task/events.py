from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import ManagedTextInput
from aiogram_dialog.widgets.kbd import Button
from bot.dialogs.state import TaskWindow
from bot.helpers import generate_task_solution

from store.actions import (
    get_tasks, get_module_by_id, get_task_by_id, add_module,
    delete_module, get_modules, add_task, delete_task, get_task_answers, get_task_answer_by_id,
    update_task_answer_by_id, add_task_answer, delete_task_answer_by_id
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


async def handle_module_info_input(message: Message,
                                   managed_input: ManagedTextInput,
                                   dialog_manager: DialogManager,
                                   text: str):
    module_name = message.text.split(":")[0].strip()
    module_number = int(message.text.split(":")[1])

    await add_module(module_number, module_name)
    modules = await get_modules()

    dialog_manager.dialog_data.update({
        "modules": modules
    })

    await dialog_manager.switch_to(
        state=TaskWindow.list
    )


async def handle_module_delete(callback: CallbackQuery, button: Button,
                               manager: DialogManager):
    selected_module = manager.dialog_data.get("selected_module")
    result = await delete_module(selected_module["id"])

    if result:
        modules = await get_modules()

        manager.dialog_data.update({
            "modules": modules,
            "selected_module": None,
            "is_module_selected": False
        })


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
                             manager: DialogManager):
    module_id = manager.dialog_data.get("selected_module")["id"]

    await add_task(title=manager.dialog_data.get("title"),
                   number=int(manager.dialog_data.get("number")),
                   module_id=module_id,
                   min_answers_count=int(manager.dialog_data.get("min_answers_count")))

    tasks = await get_tasks(module_id=module_id)

    await manager.switch_to(
        state=TaskWindow.list
    )

    manager.dialog_data.update({
        "tasks": tasks,

        "number": None,
        "title": None,
        "min_answers_count": None
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

    await manager.switch_to(
        state=TaskWindow.task_answer_edit
    )


async def handle_task_answer_action_input(callback: CallbackQuery, button: Button,
                                          manager: DialogManager):
    manager.dialog_data.update({
        "task_answer_action": button.widget_id
    })

    await callback.answer("Отправьте значение")


async def handle_task_answer_info_input(message: Message,
                                        managed_input: ManagedTextInput,
                                        dialog_manager: DialogManager,
                                        text: str):
    dialog_manager.dialog_data.update({
        dialog_manager.dialog_data.get("task_answer_action"): text
    })


async def handle_task_answer_saving(callback: CallbackQuery, button: Button,
                                    manager: DialogManager):
    task_id = manager.dialog_data.get("selected_task")["id"]
    task_answer_id = manager.dialog_data.get("task_answer_id")
    number = manager.dialog_data.get("number")
    value = manager.dialog_data.get("value")

    if task_answer_id:
        await update_task_answer_by_id(task_answer_id, number, value)

    else:
        await add_task_answer(task_id, number, value)
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


async def handle_task_answers_edit_transition(callback: CallbackQuery, button: Button,
                                              manager: DialogManager):
    await manager.switch_to(
        state=TaskWindow.task_answers_edit
    )

    manager.dialog_data.update({
        "task_answer_id": None,
        "selected_task_answer": None,

        "number": None,
        "value": None
    })


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
