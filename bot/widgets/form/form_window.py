import operator
from typing import Callable

from aiogram.fsm.state import State
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.common import Whenable
from aiogram_dialog.widgets.input import TextInput, ManagedTextInput
from aiogram_dialog.widgets.kbd import Button, Row, Select, Column
from aiogram_dialog.widgets.text import Const, Jinja, Format

from bot.utils import _loads

template = Jinja("""
<b>{{form_data['title']}}</b>

{% for key, item in form_data['model'].items() %}
<b>{{item['emoji']}}{{' ▶ ' if item['id'] == form_data['current_id'] else ' '}}{{item['title']}}</b>: {{item['value'] if item['value'] and (item['type'] != 'code') else ''}}
{% if item['type'] == 'code' %}
<pre>{{item['value']}}</pre>
{% endif %}
{% endfor %}

<i>Для изменения полей, нажмите на кнопку и введите значение</i>
""")


def get_form_data(manager: DialogManager) -> dict:
    return manager.dialog_data.get("form_data")


async def clear_payload(manager: DialogManager) -> None:
    manager.dialog_data.pop("form_data")


def model_buttons_getter(data: dict):
    return data.get("dialog_data").get("form_data").get("model_buttons")


def FormWindow(state: State) -> Window:
    async def getter(dialog_manager: DialogManager, **kwargs):
        return {
            "form_data": dialog_manager.dialog_data.get("form_data")
        }

    async def handle_back_button(callback: CallbackQuery, button: Button,
                                 manager: DialogManager):
        previous_state: State = manager.dialog_data.get("form_data").get("previous_state")

        await manager.switch_to(previous_state)
        await clear_payload(manager)

    async def handle_model_button(callback: CallbackQuery, button: Button,
                                  manager: DialogManager, item_id: str):
        form_data = get_form_data(manager)
        model_entity_id = int(item_id)

        for key, item in form_data.get("model").items():
            if item["id"] == model_entity_id:
                form_data.update({
                    "current_id": item['id']
                })

                await callback.answer(f"Отправьте '{item['title']}'")
                continue

    async def on_user_input(message: Message,
                            manager_input: ManagedTextInput,
                            dialog_manager: DialogManager,
                            text: str):
        form_data = get_form_data(dialog_manager)

        for key, item in form_data.get("model").items():
            if item['id'] == form_data['current_id']:
                item['value'] = text

                if item['id'] == form_data.get("max_id"):
                    form_data.update({
                        "current_id": 1
                    })

                else:
                    form_data.update({
                        "current_id": item['id'] + 1
                    })

                break

    def is_fields_filled(data: dict, whenable: Whenable, manager: DialogManager):
        for key, item in data.get("form_data").get("model").items():
            if item['required']:
                if not item['value']:
                    return False

        return True

    def is_delete_button_visible(data: dict, whenable: Whenable, manager: DialogManager):
        return data.get("form_data").get("show_delete_button")

    async def handle_save_button(callback: CallbackQuery, button: Button,
                                 manager: DialogManager):
        form_data = get_form_data(manager)
        handler: Callable = _loads(form_data.get("handler"))
        data = {}

        for key, item in form_data.get("model").items():
            data.update({
                key: item['value']
            })

        await handler(callback, button, manager, data)
        await clear_payload(manager)

    async def handle_delete_button(callback: CallbackQuery, button: Button,
                                   manager: DialogManager):
        form_data = get_form_data(manager)

        if form_data.get("delete_handler"):
            delete_handler: Callable = _loads(form_data.get("delete_handler"))

            await delete_handler(callback, button, manager)
            await clear_payload(manager)

    window = Window(
        template,

        Column(
            Select(
                Format("Изменить '{item[1]}'"),
                id="model_buttons",
                items=model_buttons_getter,
                on_click=handle_model_button,
                item_id_getter=operator.itemgetter(0)
            ),
        ),

        Button(
            text=Const("⠀"),
            id="separator",
        ),

        Button(
            text=Const("🔴 Удалить"),
            on_click=handle_delete_button,
            id="delete_item",
            when=is_delete_button_visible
        ),

        TextInput(
            on_success=on_user_input,
            id="form_input"
        ),

        Row(
            Button(
                text=Const("« Назад"),
                on_click=handle_back_button,
                id="form_back_button"
            ),
            Button(
                text=Const("🟢 Сохранить"),
                id="form_save_button",
                on_click=handle_save_button,
                when=is_fields_filled
            ),
        ),

        getter=getter,
        state=state
    )

    return window
