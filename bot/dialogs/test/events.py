from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import ManagedTextInput
from aiogram_dialog.widgets.kbd import Button

from ..state import TestWindow
from store.actions import get_module_by_id, get_test_answers, update_test_answer, add_test_answer, \
    get_test_answer_by_id, delete_test_answer_by_id


async def on_module_selected(callback: CallbackQuery, widget: any,
                             manager: DialogManager, item_id: str):
    module_id = int(item_id)
    module = await get_module_by_id(module_id)

    await manager.update({
        "selected_module": module,
        "is_module_selected": True
    })


async def on_module_deselect(callback: CallbackQuery, button: Button,
                             manager: DialogManager):
    await manager.update({
        "selected_module": None,
        "is_module_selected": False
    })


async def on_answers_edit(callback: CallbackQuery, button: Button,
                          manager: DialogManager):
    module_id = manager.dialog_data.get("selected_module").id
    test_answers = await get_test_answers(module_id)

    await manager.update({
        "test_answers": test_answers
    })

    await manager.switch_to(
        state=TestWindow.answers_edit
    )


async def on_new_answer(callback: CallbackQuery, widget: any,
                        manager: DialogManager):
    await manager.update({
        "selected_answer": None,
        "number": None,
        "value": None
    })

    await manager.switch_to(
        state=TestWindow.answer_edit
    )


async def on_answer_action_change(callback: CallbackQuery, button: Button,
                                  manager: DialogManager):
    await manager.update({
        "action": button.widget_id
    })

    await callback.answer("Введите значение")


async def on_answer_edit(message: Message,
                         _: ManagedTextInput,
                         dialog_manager: DialogManager,
                         text: str):
    action = dialog_manager.dialog_data.get("action")
    await dialog_manager.update({
        action: text
    })


async def on_back_to_list(callback: CallbackQuery, button: Button,
                          manager: DialogManager):
    await manager.switch_to(
        state=TestWindow.answers_edit
    )

    await manager.update({
        "selected_answer": None,
        "number": None,
        "value": None
    })


async def on_save_answer(callback: CallbackQuery, button: Button,
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

        await manager.update({
            "test_answers": test_answers
        })

        await manager.switch_to(
            state=TestWindow.answers_edit
        )

    await manager.update({
        "selected_answer": None,
        "number": None,
        "value": None
    })


async def on_answer_clicked(callback: CallbackQuery, button: Button,
                            manager: DialogManager, item_id: str):
    answer_id = int(item_id)
    selected_answer = await get_test_answer_by_id(answer_id)

    await manager.update({
        "selected_answer": selected_answer,
        "number": selected_answer.number,
        "value": selected_answer.value
    })

    await manager.switch_to(
        state=TestWindow.answer_edit
    )


async def on_answer_delete(callback: CallbackQuery, button: Button,
                           manager: DialogManager):
    answer_id = manager.dialog_data.get("selected_answer").id
    module_id = manager.dialog_data.get("selected_module").id
    await delete_test_answer_by_id(answer_id)

    test_answers = await get_test_answers(module_id)

    await manager.update({
        "test_answers": test_answers
    })

    await manager.switch_to(
        state=TestWindow.answers_edit
    )


async def on_answer_preview_clicked(callback: CallbackQuery, button: Button,
                                    manager: DialogManager, item_id: str):
    answer_id = int(item_id)
    selected_answer = await get_test_answer_by_id(answer_id)

    await manager.update({
        "selected_answer": selected_answer,
    })


async def on_show_preview(callback: CallbackQuery, button: Button,
                          manager: DialogManager):
    module_id = manager.dialog_data.get("selected_module").id
    test_answers = await get_test_answers(module_id)

    await manager.update({
        "test_answers": test_answers
    })

    await manager.switch_to(
        state=TestWindow.preview
    )


async def on_show_preview_close(callback: CallbackQuery, button: Button,
                                manager: DialogManager):
    if button.widget_id == "list":
        await manager.switch_to(
            state=TestWindow.list
        )

    else:
        await manager.done()

    await manager.update({
        "selected_answer": None
    })
