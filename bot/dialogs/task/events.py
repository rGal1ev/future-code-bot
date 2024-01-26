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


async def on_module_selected(callback: CallbackQuery, widget: any,
                             manager: DialogManager, item_id: str):
    module_id = int(item_id)

    tasks = await get_tasks(module_id)
    module = await get_module_by_id(module_id)

    await manager.update({
        "tasks": tasks,
        "is_module_selected": True,
        "selected_module": module
    })


async def on_module_deselect(callback: CallbackQuery, button: Button,
                             manager: DialogManager):
    await manager.update({
        "tasks": [],
        "is_module_selected": False
    })


async def on_task_deselect(callback: CallbackQuery, button: Button,
                           manager: DialogManager):
    await manager.update({
        "selected_task": None,
        "is_task_selected": False
    })


async def on_task_selected(callback: CallbackQuery, widget: any,
                           manager: DialogManager, item_id: str):
    task_id = int(item_id)

    task = await get_task_by_id(task_id)
    task_answers = await get_task_answers(task_id)

    await manager.update({
        "is_task_selected": True,

        "selected_task": task,
        "task_answers": task_answers
    })


async def on_new_module_update(message: Message,
                               _: ManagedTextInput,
                               dialog_manager: DialogManager,
                               __: str):
    module_name = message.text.split(":")[0].strip()
    module_number = int(message.text.split(":")[1])

    await add_module(module_number, module_name)
    modules = await get_modules()

    await dialog_manager.update({
        "modules": modules
    })

    await dialog_manager.switch_to(
        state=TaskWindow.list
    )


async def on_delete_module(callback: CallbackQuery, button: Button,
                           manager: DialogManager):
    selected_module = manager.dialog_data.get("selected_module")

    result = await delete_module(selected_module.id)

    if result:
        modules = await get_modules()

        await manager.update({
            "modules": modules,
            "selected_module": None,
            "is_module_selected": False
        })


async def on_new_task_action_change(callback: CallbackQuery, button: Button,
                                    manager: DialogManager):
    await manager.update({
        "action": button.widget_id
    })

    await callback.answer("Напишите значение")


async def on_new_task_update(message: Message,
                             _: ManagedTextInput,
                             dialog_manager: DialogManager,
                             __: str):
    action = dialog_manager.dialog_data.get("action")

    if action is None:
        action = "number"

    await dialog_manager.update({
        action: message.text
    })


async def on_task_create(callback: CallbackQuery, button: Button,
                         manager: DialogManager):
    module = manager.dialog_data.get("selected_module")

    await add_task(title=manager.dialog_data.get("title"),
                   number=int(manager.dialog_data.get("number")),
                   module_id=module.id,
                   min_answers_count=int(manager.dialog_data.get("min_answers_count")))

    tasks = await get_tasks(module_id=module.id)

    await manager.switch_to(
        state=TaskWindow.list
    )

    await manager.update({
        "tasks": tasks,

        "number": None,
        "title": None,
        "min_answers_count": None
    })


async def on_task_delete(callback: CallbackQuery, button: Button,
                         manager: DialogManager):
    task = manager.dialog_data.get("selected_task")
    await delete_task(task_id=task.id)

    tasks = await get_tasks(manager.dialog_data.get("selected_module").id)

    await manager.update({
        "selected_task": None,
        "is_task_selected": False,
        "tasks": tasks
    })


async def on_task_answer_select(callback: CallbackQuery, widget: any,
                                manager: DialogManager, item_id: str):
    task_answer_id = int(item_id)
    selected_task_answer = await get_task_answer_by_id(task_answer_id)

    await manager.update({
        "task_answer_id": item_id,

        "selected_task_answer": selected_task_answer,
        "number": selected_task_answer.number,
        "value": selected_task_answer.value
    })

    await manager.switch_to(
        state=TaskWindow.task_answer_edit
    )


async def on_new_task_answer(callback: CallbackQuery, button: Button,
                             manager: DialogManager):
    await manager.switch_to(
        state=TaskWindow.task_answer_edit
    )


async def on_task_answer_action_change(callback: CallbackQuery, button: Button,
                                       manager: DialogManager):
    await manager.update({
        "task_answer_action": button.widget_id
    })

    await callback.answer("Введите значение")


async def on_task_answer_update(message: Message,
                                _: ManagedTextInput,
                                dialog_manager: DialogManager,
                                text: str):
    await dialog_manager.update({
        dialog_manager.dialog_data.get("task_answer_action"): text
    })


async def on_task_answer_save(callback: CallbackQuery, button: Button,
                              manager: DialogManager):
    task_id = manager.dialog_data.get("selected_task").id
    task_answer_id = manager.dialog_data.get("task_answer_id")
    number = manager.dialog_data.get("number")
    value = manager.dialog_data.get("value")

    if task_answer_id:
        await update_task_answer_by_id(task_answer_id, number, value)

    else:
        await add_task_answer(task_id, number, value)
        task_answers = await get_task_answers(task_id)
        await manager.update({
            "task_answers": task_answers
        })

    await manager.switch_to(
        state=TaskWindow.task_answers_edit
    )

    await manager.update({
        "task_answer_id": None,
        "selected_task_answer": None,

        "number": None,
        "value": None
    })


async def on_back_to_answers_list(callback: CallbackQuery, button: Button,
                                  manager: DialogManager):
    await manager.switch_to(
        state=TaskWindow.task_answers_edit
    )

    await manager.update({
        "task_answer_id": None,
        "selected_task_answer": None,

        "number": None,
        "value": None
    })


async def on_task_answer_delete(callback: CallbackQuery, button: Button,
                                manager: DialogManager):
    task_id = manager.dialog_data.get("selected_task").id
    task_answer_id = manager.dialog_data.get("task_answer_id")

    await delete_task_answer_by_id(task_answer_id)
    task_answers = await get_task_answers(task_id)

    await manager.update({
        "task_answers": task_answers
    })

    await manager.switch_to(
        state=TaskWindow.task_answers_edit
    )

    await manager.update({
        "task_answer_id": None,
        "selected_task_answer": None,

        "number": None,
        "value": None
    })


async def on_task_purpose_generate(callback: CallbackQuery, button: Button,
                                   manager: DialogManager):
    task = manager.dialog_data.get("selected_task")
    task_answers = manager.dialog_data.get("task_answers")
    solution = generate_task_solution(task, task_answers)

    await manager.update({
        "solution": solution
    })
    await manager.switch_to(
        state=TaskWindow.preview
    )
