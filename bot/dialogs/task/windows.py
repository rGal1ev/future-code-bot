from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import (
    Cancel, Select, Column, Button, Row, SwitchTo, ScrollingGroup, Url, NextPage, PrevPage
)
from aiogram_dialog.widgets.text import Const, Format

from .events import (
    handle_module_select, handle_module_deselect, handle_task_select, handle_task_deselect,
    handle_task_create, handle_task_answer_select,
    handle_task_solution_generate, handle_task_answer_form_creation, handle_module_edit, handle_module_create,
    handle_task_edit, handle_file_sending
)
from .templates import (
    main_window_template, solution_preview_window_template,
    task_answers_edit_window_template
)
from .data import (
    list_window_data,
    answer_tasks_data, solution_preview_data
)

from ..state import TaskWindow
from ...utils import _and, _not, _get
from ...widgets.form import FormTrigger


list_window = Window(
    main_window_template,

    Column(
        Column(
            Select(
                Format("» {item[number]} - {item[title]}"),

                items="modules",
                item_id_getter=_get("id"),
                id="module_list",

                on_click=handle_module_select
            ),

            Button(
                text=Const("⠀"),
                id="separator"
            ),
            FormTrigger(
                text=Const("🟢 Добавить модуль"),
                title="💡 Создание модуля",
                state=TaskWindow.form,
                model={
                    "number": {
                        "title": "Номер",
                        "emoji": "❶",
                        "required": True,
                        "default": 0,
                    },
                    "title": {
                        "title": "Название",
                        "emoji": "❷",
                        "required": True,
                        "default": ""
                    },
                },

                id="add_new_module",
                handler=handle_module_create,
                when="is_admin"
            ),
            when=_not("is_module_selected")
        ),

        Column(
            Select(
                Format("» {item[number]} - {item[title]}"),

                items="tasks",
                item_id_getter=_get("id"),
                id="task_list",

                on_click=handle_task_select
            ),
            Button(
                text=Const("⠀"),
                id="separator",
            ),
            FormTrigger(
                text=Const("🟢 Добавить работу"),
                title="💡 Создание работы",
                state=TaskWindow.form,
                model={
                    "number": {
                        "title": "Номер",
                        "emoji": "❶",
                        "required": True,
                        "default": 0,
                    },
                    "title": {
                        "title": "Название",
                        "emoji": "❷",
                        "required": True,
                        "default": ""
                    },
                    "min_answers_count": {
                        "title": "Минимальное кол-во ответов",
                        "emoji": "❸",
                        "required": True,
                        "default": 0
                    }
                },

                id="add_new_task",
                handler=handle_task_create,
                when="is_admin"
            ),
            Button(
                text=Const("✏️ Редактировать модуль"),
                on_click=handle_module_edit,
                id="edit_module",
                when="is_admin"
            ),
            when="is_module_selected"
        ),
        when=_and("!is_module_selected", "!is_task_selected")
    ),

    Column(
        Button(
            text=Const("↻ Сгенерировать ответ"),
            id="generate_task",
            on_click=handle_task_solution_generate
        ),
        Button(
            text=Const("⠀"),
            id="separator",
        ),
        Button(
            text=Const("✏️ Редактировать работу"),
            on_click=handle_task_edit,
            id="edit_task",
            when="is_admin"
        ),
        SwitchTo(
            text=Const("✏️ Редактировать ответы"),
            id="edit_task_answers",
            state=TaskWindow.task_answers_edit,
            when="is_admin"
        ),

        when=_and("is_module_selected", "is_task_selected")
    ),

    Row(
        Button(
            text=Const("« Назад"),
            id="deselect_task",
            on_click=handle_task_deselect,
            when=_and("is_module_selected", "is_task_selected")
        ),

        Row(
            Button(
                text=Const("« Назад"),
                id="deselect_module",
                on_click=handle_module_deselect,
                when="is_module_selected"
            ),
            when=_and("!is_module_selected", "!is_task_selected")
        ),

        Cancel(
            text=Const("☰ Выйти")
        ),
    ),

    getter=list_window_data,
    state=TaskWindow.list
)

task_answers_edit_window = Window(
    task_answers_edit_window_template,

    ScrollingGroup(
        Select(
            items="task_answers",
            id="task_answers_list",
            text=Format("» {item[number]} Вопрос"),
            item_id_getter=_get("id"),
            on_click=handle_task_answer_select
        ),

        width=1,
        height=4,
        hide_pager=True,
        id="task_answers_list_paginator"
    ),

    Row(
        PrevPage(
            text=Const("◀"),
            scroll="task_answers_list_paginator"
        ),
        NextPage(
            text=Const("▶"),
            scroll="task_answers_list_paginator"
        )
    ),

    Row(
        SwitchTo(
            text=Const("« Назад"),
            state=TaskWindow.list,
            id="back_to_list"
        ),
        FormTrigger(
            text=Const("🟢 Добавить"),
            title="💡 Создание ответа",
            state=TaskWindow.form,
            model={
                "number": {
                    "title": "Номер",
                    "emoji": "❶",
                    "required": True,
                    "default": 0,
                },
                "value": {
                    "title": "Ответ",
                    "emoji": "❷",
                    "type": "code",
                    "required": True,
                    "default": ""
                }
            },

            id="add_new_task_answer",
            handler=handle_task_answer_form_creation,
        ),
    ),

    getter=answer_tasks_data,
    state=TaskWindow.task_answers_edit
)

solution_preview_window = Window(
    solution_preview_window_template,

    Row(
        SwitchTo(
            text=Const("« Назад"),
            id="back_to_list",
            state=TaskWindow.list
        ),
        Url(
            text=Const("Открыть сайт"),
            url=Const("https://online-vstu.ru/login")
        )
    ),

    Button(
        text=Const("Получить в виде файла"),
        on_click=handle_file_sending,
        id="get_as_file"
    ),

    getter=solution_preview_data,
    state=TaskWindow.preview
)
