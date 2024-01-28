from typing import Callable
from aiogram.fsm.state import State
from aiogram_dialog import DialogManager
from .helpers import use_models
from ...utils import _dumps


async def trigger_form(manager: DialogManager,
                       state: State,
                       model: dict,
                       handler: Callable,
                       title: str | None = "Заполните поля ниже",
                       show_delete_button: bool = False,
                       delete_handler: Callable = None) -> None:
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
