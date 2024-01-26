from aiogram_dialog import Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Cancel, Select, Column, Button, Row, ScrollingGroup, SwitchTo
from aiogram_dialog.widgets.text import Const, Format, Jinja

from .data import list_window_data, answers_edit_data, test_preview_data
from .events import on_module_selected, on_module_deselect, on_answers_edit, on_new_answer, on_answer_action_change, \
    on_answer_edit, on_back_to_list, on_save_answer, on_answer_clicked, on_answer_delete, on_answer_preview_clicked, \
    on_show_preview, on_show_preview_close
from .templates import list_window_template, answer_edit_window_template, test_preview_window_template
from .utils import module_id_getter, not_is_module_selected, test_id_getter, is_answer_ready
from ..state import TestWindow

list_window = Window(
    list_window_template,

    Column(
        Select(
            Format("» {item.number} - {item.title}"),

            items="modules",
            item_id_getter=module_id_getter,
            id="module_list",

            on_click=on_module_selected
        ),
        when=not_is_module_selected
    ),

    Column(
        Button(
            text=Const("Показать ответы"),
            id="start_test",
            on_click=on_show_preview,
        ),

        Button(
            text=Const("⠀"),
            id="separator",
            when="is_admin"
        ),

        Button(
            text=Const("✏️ Редактировать ответы"),
            id="edit_answers",
            on_click=on_answers_edit,
            when="is_admin"
        ),

        when="is_module_selected"
    ),

    Row(
        Button(
            text=Const("« Назад"),
            id="deselect_module",
            on_click=on_module_deselect,
            when="is_module_selected"
        ),
        Cancel(
            text=Const("☰ Выйти")
        ),
    ),

    getter=list_window_data,
    state=TestWindow.list
)

answers_edit_window = Window(
    Const("<b>Редактирование ответов теста</b>"),
    ScrollingGroup(
        Select(
            Format("» Вопрос {item.number}"),

            items="test_answers",
            item_id_getter=test_id_getter,
            id="test_list",
            on_click=on_answer_clicked
        ),

        width=1,
        height=4,
        hide_on_single_page=True,
        id="test_answers_list_paginator"
    ),
    Row(
        SwitchTo(
            text=Const("« Назад"),
            id="back_to_list",
            state=TestWindow.list
        ),
        Button(
            text=Const("🟢 Добавить"),
            id="add_new_answer",
            on_click=on_new_answer
        ),
    ),

    getter=answers_edit_data,
    state=TestWindow.answers_edit
)

answer_edit_window = Window(
    answer_edit_window_template,
    TextInput(
        id="on_answer_edit",
        on_success=on_answer_edit
    ),
    Button(
        text=Jinja("""{{ '✓ ' if number else '' }}Указать номер"""),
        on_click=on_answer_action_change,
        id="number"
    ),
    Button(
        text=Jinja("""{{ '✓ ' if value else '' }}Указать ответ"""),
        on_click=on_answer_action_change,
        id="value"
    ),

    Button(
        text=Const("⠀"),
        id="separator",
        when="is_admin"
        ),

    Button(
        text=Const("🔴 Удалить"),
        on_click=on_answer_delete,
        id="delete_answer",
        when="selected_answer"
    ),

    Row(
        Button(
            text=Const("« Назад"),
            id="back_to_list",
            on_click=on_back_to_list
        ),
        Button(
            text=Const("🟢 Сохранить"),
            id="save_answer",
            on_click=on_save_answer,
            when=is_answer_ready
        ),
    ),

    getter=answers_edit_data,
    state=TestWindow.answer_edit
)


test_preview_window = Window(
    test_preview_window_template,
    Button(
        text=Jinja("""{{ 'Выбран » ' + selected_answer.number|string if selected_answer else 'Не выбрано' }}"""),
        id="current_answer"
    ),
    ScrollingGroup(
        Select(
            Jinja("""» Вопрос {{item.number}}"""),

            items="test_answers",
            item_id_getter=test_id_getter,
            id="test_list",
            on_click=on_answer_preview_clicked
        ),

        width=1,
        height=4,
        hide_on_single_page=True,
        id="test_answers_list_paginator"
    ),

    Row(
        Button(
            text=Const("« Назад"),
            id="list",
            on_click=on_show_preview_close
        ),
        Button(
            text=Const("☰ Выйти"),
            id="menu",
            on_click=on_show_preview_close
        )
    ),

    getter=test_preview_data,
    state=TestWindow.preview
)
