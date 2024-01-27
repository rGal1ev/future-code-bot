import base64
from typing import Callable

from aiogram.fsm.state import State
from aiogram.types import CallbackQuery
from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.kbd import Button, Row
from aiogram_dialog.widgets.text import Const, Format, Jinja
from pickle import loads

from bot.widgets.alert.alert_data import generate_alert_data

template = Jinja("""
⚠️ <b>{{ alert_title }}</b>
─────────
{% if alert_description %}
{{ alert_description }}
{% endif %}
""")


def AlertWindow(state: State) -> Window:
    async def getter(dialog_manager: DialogManager, **kwargs):
        return generate_alert_data(dialog_manager)

    async def clear_alert_payload(manager: DialogManager):
        manager.dialog_data.update(generate_alert_data(manager))

    async def handle_back_button(callback: CallbackQuery, button: Button,
                                 manager: DialogManager):
        previous_state: State = manager.dialog_data.get("alert_previous_state")

        await manager.switch_to(previous_state)
        await clear_alert_payload(manager)

    async def handle_process_button(callback: CallbackQuery, button: Button,
                                    manager: DialogManager):
        handler_string = manager.dialog_data.get("alert_handler")
        handler_bytes = base64.b64decode(handler_string)
        handler: Callable = loads(handler_bytes)

        await handler(callback, button, manager)
        await clear_alert_payload(manager)

    alert_window = Window(
        template,

        Row(
            Button(
                text=Format("{alert_back_button_text}"),
                id="alert_back_button",
                on_click=handle_back_button
            ),

            Button(
                text=Format("{alert_process_button_text}"),
                id="alert_process_button",
                on_click=handle_process_button
            ),
        ),

        getter=getter,
        state=state
    )

    return alert_window
