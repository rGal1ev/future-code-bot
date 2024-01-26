from aiogram.types import CallbackQuery
from aiogram_dialog import Window, DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Row, Button, Url, Column, Start
from aiogram_dialog.widgets.text import Const, Text
from ..state import MainWindow, TaskWindow
from os import getenv


async def handle_task(callback: CallbackQuery, button: Button,
                      manager: DialogManager):
    is_user_admin = str(callback.from_user.id) in getenv("ADMIN_ID")

    await manager.start(
        state=TaskWindow.list,
        data={
            "is_admin": is_user_admin
        }
    )


main_window = Window(
    Const(
        text="#КодБудущего"
    ),
    Column(
        Button(
            text=Const("Самостоятельные"),
            id="handle_task",
            on_click=handle_task
        ),
        Button(
            text=Const("Аттестации"),
            id="empty",
        ),
    ),

    Row(
        Url(
            text=Const("Сайт"),
            url=Const("https://online-vstu.ru/login")
        ),
        Url(
            text=Const("Учитель"),
            url=Const("https://t.me/rgal1ev")
        )
    ),

    state=MainWindow.main
)
