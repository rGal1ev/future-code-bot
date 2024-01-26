from aiogram_dialog import Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Cancel, Select, Column, Button, Row, SwitchTo, Back, ScrollingGroup, Url
from aiogram_dialog.widgets.text import Const, Format, Jinja

from .events import (
    on_module_selected, on_module_deselect, on_task_selected, on_task_deselect, on_new_module_update,
    on_delete_module, on_new_task_action_change, on_new_task_update, on_task_create, on_task_delete,
    on_task_answer_select, on_task_answer_action_change, on_task_answer_update, on_task_answer_save, on_new_task_answer,
    on_task_answer_delete, on_back_to_answers_list, on_task_purpose_generate
)
from .utils import (
    module_id_getter, is_module_not_selected, task_id_getter, is_ready_to_generate,
    not_is_ready_to_generate, is_task_ready, task_answer_id_getter
)

from ..state import TaskWindow
from .templates import main_window_template, new_module_window_template, new_task_window_template, \
    task_answer_edit_window_template
from .data import list_window_data, new_module_data, new_task_data, answer_tasks_data, solution_preview_data

list_window = Window(
    main_window_template,
    Column(
        Column(
            Select(
                Format("» {item.number} - {item.title}"),

                items="modules",
                item_id_getter=module_id_getter,
                id="module_list",

                on_click=on_module_selected
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
            when=is_module_not_selected
        ),

        Column(
            Select(
                Format("» {item.number} - {item.title}"),

                items="tasks",
                item_id_getter=task_id_getter,
                id="task_list",

                on_click=on_task_selected
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
            Button(
                id="delete_module",
                text=Const("🔴 Удалить модуль"),
                on_click=on_delete_module,
                when="is_admin"
            ),
            when="is_module_selected"
        ),
        when=not_is_ready_to_generate
    ),

    Column(
        Button(
            text=Const("↻ Сгенерировать ответ"),
            id="generate_task",
            on_click=on_task_purpose_generate
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
        Button(
            id="delete_task",
            text=Const("🔴 Удалить работу"),
            on_click=on_task_delete,
            when="is_admin"
        ),
        when=is_ready_to_generate
    ),

    Row(
        Button(
            text=Const("« Назад"),
            id="deselect_task",
            on_click=on_task_deselect,
            when=is_ready_to_generate
        ),

        Row(
            Button(
                text=Const("« Назад"),
                id="deselect_module",
                on_click=on_module_deselect,
                when="is_module_selected"
            ),
            when=not_is_ready_to_generate
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
        on_success=on_new_module_update,
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
        on_success=on_new_task_update
    ),
    Button(
        text=Jinja("""{{ '✓ ' if number else '' }}Указать номер"""),
        on_click=on_new_task_action_change,
        id="number"
    ),
    Button(
        text=Jinja("""{{ '✓ ' if title else '' }}Указать название"""),
        on_click=on_new_task_action_change,
        id="title"
    ),
    Button(
        text=Jinja("""{{ '✓ ' if min_answers_count else '' }}Указать количество"""),
        on_click=on_new_task_action_change,
        id="min_answers_count"
    ),

    Button(
        text=Const("🟢 Создать"),
        id="create_task",
        on_click=on_task_create,
        when=is_task_ready
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
    Const("<b>Редактирование ответов</b>"),

    ScrollingGroup(
        Select(
            items="task_answers",
            id="task_answers_list",
            text=Format("» {item.number} Вопрос"),
            item_id_getter=task_answer_id_getter,
            on_click=on_task_answer_select
        ),

        width=1,
        height=4,
        hide_on_single_page=True,
        id="task_answers_list_paginator"
    ),

    Row(
        SwitchTo(
            text=Const("« Назад"),
            state=TaskWindow.list,
            id="back_to_list"
        ),
        Button(
            text=Const("🟢 Добавить"),
            id="add_new_task_answer",
            on_click=on_new_task_answer
        )
    ),

    getter=answer_tasks_data,
    state=TaskWindow.task_answers_edit
)

task_answer_edit_window = Window(
    task_answer_edit_window_template,

    TextInput(
        on_success=on_task_answer_update,
        id="task_answer_info",
    ),

    Button(
        text=Jinja("""{{ '✓ ' if number else '' }}Указать номер"""),
        on_click=on_task_answer_action_change,
        id="number"
    ),
    Button(
        text=Jinja("""{{ '✓ ' if value else '' }}Указать ответ"""),
        on_click=on_task_answer_action_change,
        id="value"
    ),

    Button(
        text=Const("⠀"),
        id="separator",
        when="is_admin"
    ),

    Button(
        text=Const("🔴 Удалить ответ"),
        on_click=on_task_answer_delete,
        id="empty",
        when="task_answer_id"
    ),

    Row(
        Button(
            text=Const("« Назад"),
            on_click=on_back_to_answers_list,
            id="back_to_list"
        ),
        Button(
            text=Const("🟢 Сохранить"),
            id="save_task_answer",
            on_click=on_task_answer_save
        )
    ),

    getter=answer_tasks_data,
    state=TaskWindow.task_answer_edit
)


solution_preview_window = Window(
    Jinja("""<pre language="python">{{solution}}</pre>"""),

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
