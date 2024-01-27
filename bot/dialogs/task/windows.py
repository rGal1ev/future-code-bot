from aiogram.types import CallbackQuery
from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import (
    Cancel, Select, Column, Button, Row, SwitchTo, Back, ScrollingGroup, Url, NextPage, PrevPage
)
from aiogram_dialog.widgets.text import Const, Format, Jinja

from .events import (
    handle_module_select, handle_module_deselect, handle_task_select, handle_task_deselect,
    handle_module_info_input, handle_module_delete, handle_task_action_change, handle_task_info_input,
    handle_task_create, handle_task_delete, handle_task_answer_select, handle_task_answer_action_input,
    handle_task_answer_info_input, handle_task_answer_saving, handle_task_answer_delete,
    handle_task_answers_edit_transition, handle_task_solution_generate
)
from .templates import (
    main_window_template, new_module_window_template, new_task_window_template,
    task_answer_edit_window_template, solution_preview_window_template, task_answers_edit_window_template
)
from .data import (
    list_window_data, new_module_data, new_task_data,
    answer_tasks_data, solution_preview_data
)

from ..state import TaskWindow
from ...utils import _and, _not, _get
from ...widgets.alert import AlertTrigger

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
                id="separator",
                when="is_admin"
            ),
            SwitchTo(
                text=Const("🟢 Добавить модуль"),
                id="add_module",
                state=TaskWindow.new_module,
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
                when="is_admin"
            ),
            SwitchTo(
                text=Const("🟢 Добавить работу"),
                id="add_task",
                state=TaskWindow.new_task,
                when="is_admin"
            ),
            AlertTrigger(
                text=Const("🔴 Удалить модуль"),
                state=TaskWindow.alert,

                title="Удалить модуль?",
                description="Восстановить модуль будет невозможно",
                on_process=handle_module_delete,

                id="show_alert",
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
            when="is_admin"
        ),
        SwitchTo(
            text=Const("✏️ Редактировать ответы"),
            id="edit_task_answers",
            state=TaskWindow.task_answers_edit,
            when="is_admin"
        ),
        AlertTrigger(
            text=Const("🔴 Удалить работу"),
            state=TaskWindow.alert,

            title="Удалить работу?",
            description="Восстановить работу будет невозможно",
            on_process=handle_task_delete,

            id="show_alert",
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

new_module_window = Window(
    new_module_window_template,

    TextInput(
        on_success=handle_module_info_input,
        id="module_info",
    ),
    Back(
        text=Const("« Назад")
    ),

    getter=new_module_data,
    state=TaskWindow.new_module
)


new_task_window = Window(
    new_task_window_template,
    TextInput(
        id="task_info",
        on_success=handle_task_info_input
    ),
    Button(
        text=Jinja("""{{ '✓ ' if number else '' }}Указать номер"""),
        on_click=handle_task_action_change,
        id="number"
    ),
    Button(
        text=Jinja("""{{ '✓ ' if title else '' }}Указать название"""),
        on_click=handle_task_action_change,
        id="title"
    ),
    Button(
        text=Jinja("""{{ '✓ ' if min_answers_count else '' }}Указать количество"""),
        on_click=handle_task_action_change,
        id="min_answers_count"
    ),

    Button(
        text=Const("🟢 Создать"),
        id="create_task",
        on_click=handle_task_create,
        when=_and("number", "title", "min_answers_count")
    ),

    SwitchTo(
        text=Const("« Назад"),
        state=TaskWindow.list,
        id="back_to_list"

    ),

    getter=new_task_data,
    state=TaskWindow.new_task
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
        SwitchTo(
            text=Const("🟢 Добавить"),
            id="add_new_task_answer",
            state=TaskWindow.task_answer_edit
        )
    ),

    getter=answer_tasks_data,
    state=TaskWindow.task_answers_edit
)

task_answer_edit_window = Window(
    task_answer_edit_window_template,

    TextInput(
        on_success=handle_task_answer_info_input,
        id="task_answer_info",
    ),

    Button(
        text=Jinja("""{{ '✓ ' if number else '' }}Указать номер"""),
        on_click=handle_task_answer_action_input,
        id="number"
    ),
    Button(
        text=Jinja("""{{ '✓ ' if value else '' }}Указать ответ"""),
        on_click=handle_task_answer_action_input,
        id="value"
    ),

    Button(
        text=Const("⠀"),
        id="separator",
        when="is_admin"
    ),

    AlertTrigger(
        text=Const("🔴 Удалить ответ"),
        state=TaskWindow.alert,

        title="Удалить ответ?",
        description="Восстановить ответ будет невозможно",
        on_process=handle_task_answer_delete,

        id="show_alert",
        when="task_answer_id"
    ),

    Row(
        Button(
            text=Const("« Назад"),
            on_click=handle_task_answers_edit_transition,
            id="back_to_list"
        ),
        Button(
            text=Const("🟢 Сохранить"),
            id="save_task_answer",
            on_click=handle_task_answer_saving
        )
    ),

    getter=answer_tasks_data,
    state=TaskWindow.task_answer_edit
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

    getter=solution_preview_data,
    state=TaskWindow.preview
)
