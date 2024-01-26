from aiogram.methods import Close
from aiogram.types import CallbackQuery
from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.kbd import Button, Url, Column, Row, Cancel
from aiogram_dialog.widgets.text import Const

from .templates import main_window_template
from ..state import MainWindow, TaskWindow, TestWindow
from os import getenv


async def handle_switch(callback: CallbackQuery, button: Button,
                        manager: DialogManager):
    is_user_admin = str(callback.from_user.id) in getenv("ADMIN_ID")

    if button.widget_id == "task":
        await manager.start(
            state=TaskWindow.list,
            data={
                "is_admin": is_user_admin
            }
        )

    else:
        await manager.start(
            state=TestWindow.list,
            data={
                "is_admin": is_user_admin
            }
        )


main_window = Window(
    main_window_template,
    Column(
        Button(
            text=Const("❶ Самостоятельные"),
            id="task",
            on_click=handle_switch
        ),
        Button(
            text=Const("❷ Аттестации"),
            id="test",
            on_click=handle_switch
        ),
    ),

    Row(
        Cancel(
            text=Const("✖ Завершить")
        ),
        Url(
            text=Const("🌐 Сайт"),
            url=Const("https://online-vstu.ru/login")
        ),
    ),

    state=MainWindow.main
)
