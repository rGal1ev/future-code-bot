from aiogram_dialog import Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Cancel, Select, Column, Button, Row, ScrollingGroup, SwitchTo
from aiogram_dialog.widgets.text import Const, Format, Jinja

from .events import (
    handle_module_select, handle_module_deselect, handle_answers_edit_transition,
    handle_answer_edit_transition, handle_answer_action_change, handle_user_answer_info_input,
    handle_back_to_answers_edit_transition, handle_answer_saving, handle_answer_select, handle_answer_delete,
    handle_answer_preview_select, handle_preview_transition, handle_dynamically_transition
)

from .templates import list_window_template, answer_edit_window_template, test_preview_window_template
from .data import list_window_data, answers_edit_data, test_preview_data
from ..state import TestWindow
from ...utils import _get, _not, _and
from ...widgets.alert import AlertTrigger

list_window = Window(
    list_window_template,

    Column(
        Select(
            Format("» {item[number]} - {item[title]}"),

            items="modules",
            item_id_getter=_get("id"),
            id="module_list",

            on_click=handle_module_select
        ),
        when=_not("is_module_selected")
    ),

    Column(
        Button(
            text=Const("Показать ответы"),
            id="start_test",
            on_click=handle_preview_transition,
        ),

        Button(
            text=Const("⠀"),
            id="separator",
            when="is_admin"
        ),

        Button(
            text=Const("✏️ Редактировать ответы"),
            id="edit_answers",
            on_click=handle_answers_edit_transition,
            when="is_admin"
        ),

        when="is_module_selected"
    ),

    Row(
        Button(
            text=Const("« Назад"),
            id="deselect_module",
            on_click=handle_module_deselect,
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
            Format("» Вопрос {item[number]}"),

            items="test_answers",
            item_id_getter=_get("id"),
            id="test_list",
            on_click=handle_answer_select
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
            on_click=handle_answer_edit_transition
        ),
    ),

    getter=answers_edit_data,
    state=TestWindow.answers_edit
)

answer_edit_window = Window(
    answer_edit_window_template,
    TextInput(
        id="answer_info",
        on_success=handle_user_answer_info_input
    ),
    Button(
        text=Jinja("""{{ '✓ ' if number else '' }}Указать номер"""),
        on_click=handle_answer_action_change,
        id="number"
    ),
    Button(
        text=Jinja("""{{ '✓ ' if value else '' }}Указать ответ"""),
        on_click=handle_answer_action_change,
        id="value"
    ),

    Button(
        text=Const("⠀"),
        id="separator",
        when="is_admin"
        ),

    AlertTrigger(
        text=Const("🔴 Удалить"),
        state=TestWindow.alert,

        title="Удалить ответ?",
        description="Восстановить ответ будет невозможно",
        on_process=handle_answer_delete,

        id="show_alert",
        when="selected_answer"
    ),

    Row(
        Button(
            text=Const("« Назад"),
            id="back_to_list",
            on_click=handle_back_to_answers_edit_transition
        ),
        Button(
            text=Const("🟢 Сохранить"),
            id="save_answer",
            on_click=handle_answer_saving,
            when=_and("number", "value")
        ),
    ),

    getter=answers_edit_data,
    state=TestWindow.answer_edit
)


test_preview_window = Window(
    test_preview_window_template,
    Button(
        text=Jinja(
            """{{ 'Выбран » ' + selected_answer['number']|string if selected_answer else 'Не выбрано' }}"""
        ),
        id="current_answer"
    ),
    ScrollingGroup(
        Select(
            Jinja("""» Вопрос {{item['number']}}"""),

            items="test_answers",
            item_id_getter=_get("id"),
            id="test_list",
            on_click=handle_answer_preview_select
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
            on_click=handle_dynamically_transition
        ),
        Button(
            text=Const("☰ Выйти"),
            id="menu",
            on_click=handle_dynamically_transition
        )
    ),

    getter=test_preview_data,
    state=TestWindow.preview
)
