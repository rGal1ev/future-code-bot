import pprint
from typing import Callable
from aiogram.fsm.state import State
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.common import WhenCondition
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Text
from .helpers import use_models
from ...utils import _dumps


def FormTrigger(text: Text,
                id: str,
                state: State,
                model: dict,
                handler: Callable,
                title: str | None = "Заполните поля ниже",
                show_delete_button: bool = False,
                delete_handler: Callable = None,
                when: WhenCondition | None = None) -> Button:
    async def button_handler(callback: CallbackQuery, button: Button,
                             manager: DialogManager):
        prepared_model, model_buttons, max_id = use_models(model)

        form_payload = {
            "previous_state": _dumps(manager.current_context().state),
            "model": prepared_model,
            "model_buttons": model_buttons,
            "handler": _dumps(handler),

            "current_id": 1,
            "max_id": max_id,

            "title": title,
            "show_delete_button": show_delete_button,
            "delete_handler": _dumps(delete_handler)
        }

        await manager.update({
            "form_data": {
                **form_payload
            }
        })

        await manager.switch_to(state)

    trigger_button = Button(
        text=text,
        on_click=button_handler,
        when=when,
        id=id
    )

    return trigger_button
