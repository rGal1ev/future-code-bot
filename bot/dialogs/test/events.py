from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import ManagedTextInput
from aiogram_dialog.widgets.kbd import Button

from store.actions import (
    get_module_by_id, get_test_answers, update_test_answer,
    add_test_answer, get_test_answer_by_id, delete_test_answer_by_id
)

from ..state import TestWindow


async def handle_module_select(callback: CallbackQuery, widget: any,
                               manager: DialogManager, item_id: str):
    module_id = int(item_id)
    module = await get_module_by_id(module_id)

    manager.dialog_data.update({
        "selected_module": module,
        "is_module_selected": True
    })


async def handle_module_deselect(callback: CallbackQuery, button: Button,
                                 manager: DialogManager):
    manager.dialog_data.update({
        "selected_module": None,
        "is_module_selected": False
    })


async def handle_answers_edit_transition(callback: CallbackQuery, button: Button,
                                         manager: DialogManager):
    module_id = manager.dialog_data.get("selected_module").id
    test_answers = await get_test_answers(module_id)

    manager.dialog_data.update({
        "test_answers": test_answers
    })

    await manager.switch_to(
        state=TestWindow.answers_edit
    )


async def handle_answer_edit_transition(callback: CallbackQuery, widget: any,
                                        manager: DialogManager):
    await manager.update({
        "selected_answer": None,
        "number": None,
        "value": None
    })
    await manager.switch_to(
        state=TestWindow.answer_edit
    )


async def handle_answer_action_change(callback: CallbackQuery, button: Button,
                                      manager: DialogManager):
    await manager.update({
        "action": button.widget_id
    })
    await callback.answer("Введите значение")


async def handle_user_answer_info_input(message: Message,
                                        managed_input: ManagedTextInput,
                                        dialog_manager: DialogManager,
                                        text: str):
    action = dialog_manager.dialog_data.get("action")
    dialog_manager.dialog_data.update({
        action: text
    })


async def handle_back_to_answers_edit_transition(callback: CallbackQuery, button: Button,
                                                 manager: DialogManager):
    await manager.switch_to(
        state=TestWindow.answers_edit
    )

    manager.dialog_data.update({
        "selected_answer": None,
        "number": None,
        "value": None
    })


async def handle_answer_saving(callback: CallbackQuery, button: Button,
                               manager: DialogManager):
    selected_answer = manager.dialog_data.get("selected_answer")
    selected_module = manager.dialog_data.get("selected_module")

    number = manager.dialog_data.get("number")
    value = manager.dialog_data.get("value")

    if selected_answer:
        await update_test_answer(selected_answer.id, number, value)
        await manager.switch_to(
            state=TestWindow.answers_edit
        )

    else:
        await add_test_answer(selected_module.id, number, value)
        test_answers = await get_test_answers(selected_module.id)

        manager.dialog_data.update({
            "test_answers": test_answers
        })

        await manager.switch_to(
            state=TestWindow.answers_edit
        )

    manager.dialog_data.update({
        "selected_answer": None,
        "number": None,
        "value": None
    })


async def handle_answer_select(callback: CallbackQuery, button: Button,
                               manager: DialogManager, item_id: str):
    answer_id = int(item_id)
    selected_answer = await get_test_answer_by_id(answer_id)

    manager.dialog_data.update({
        "selected_answer": selected_answer,
        "number": selected_answer.number,
        "value": selected_answer.value
    })

    await manager.switch_to(
        state=TestWindow.answer_edit
    )


async def handle_answer_delete(callback: CallbackQuery, button: Button,
                               manager: DialogManager):
    answer_id = manager.dialog_data.get("selected_answer").id
    module_id = manager.dialog_data.get("selected_module").id

    await delete_test_answer_by_id(answer_id)
    test_answers = await get_test_answers(module_id)

    manager.dialog_data.update({
        "test_answers": test_answers
    })

    await manager.switch_to(
        state=TestWindow.answers_edit
    )


async def handle_answer_preview_select(callback: CallbackQuery, button: Button,
                                       manager: DialogManager, item_id: str):
    answer_id = int(item_id)
    selected_answer = await get_test_answer_by_id(answer_id)

    manager.dialog_data.update({
        "selected_answer": selected_answer,
    })


async def handle_preview_transition(callback: CallbackQuery, button: Button,
                                    manager: DialogManager):
    module_id = manager.dialog_data.get("selected_module").id
    test_answers = await get_test_answers(module_id)

    manager.dialog_data.update({
        "test_answers": test_answers
    })

    await manager.switch_to(
        state=TestWindow.preview
    )


async def handle_dynamically_transition(callback: CallbackQuery, button: Button,
                                        manager: DialogManager):
    if button.widget_id == "list":
        await manager.switch_to(
            state=TestWindow.list
        )

    else:
        await manager.done()

    manager.dialog_data.update({
        "selected_answer": None
    })
