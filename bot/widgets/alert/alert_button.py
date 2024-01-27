import base64
import pprint
from typing import Union

from aiogram.fsm.state import State
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.common import WhenCondition
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.kbd.button import OnClick
from aiogram_dialog.widgets.text import Text
from aiogram_dialog.widgets.widget_event import WidgetEventProcessor
import pickle


def AlertTrigger(text: Text,
                 id: str,
                 state: State,
                 title: str,
                 on_process: Union[OnClick, WidgetEventProcessor, None],
                 when: WhenCondition = None,
                 description: str | None = None,
                 process_button_text: str = "Подтвердить",
                 back_button_text: str | None = "Назад") -> Button:
    async def alert_button_handler(callback: CallbackQuery, button: Button,
                                   manager: DialogManager):
        handler_bytes = pickle.dumps(on_process)
        handler_string = base64.b64encode(handler_bytes).decode("UTF-8")

        alert_payload = {
            "alert_title": title,
            "alert_description": description,
            "alert_handler":  handler_string,
            "alert_process_button_text": process_button_text,
            "alert_back_button_text": back_button_text,
            "alert_previous_state": manager.current_context().state
        }

        await manager.update(alert_payload)
        await manager.switch_to(
            state=state
        )

    alert_button = Button(
        text=text,
        on_click=alert_button_handler,
        id=id,
        when=when
    )

    return alert_button
