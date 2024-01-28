from aiogram_dialog.widgets.text import Jinja

main_window_template = Jinja("""
<b>📝 Самостоятельные работы</b>

{% if is_module_selected %}
{% if selected_module %}
─────────
✦ Выбран <b>{{ selected_module["number"] }}</b> модуль
➤ <b>{{ selected_module["title"] }}</b>
{% endif %}
{% if is_task_selected %}
───
✦ Выбрана <b>{{ selected_task["number"] }}</b> работа 
➤ <b>{{ selected_task["title"] }}</b>
─────────

▼ Получить ответ
{% else %}

❷ Выберите самостоятельную работу
{% endif %}

{% else %}
❶ Выберите модуль
{% endif %}
""")

solution_preview_window_template = Jinja("""
{% if solution == "empty" %}
<b>Решение самостоятельной не заполнено</b>
{% else %}
<pre language="python">{{solution}}</pre>
{% endif %}
""")

task_answers_edit_window_template = Jinja("""
✏️ <b>Ответы самостоятельной работы</b>

<b>Доступно</b>:
❶ Создание
❷ Редактирование

<i>Выберите ответ в списке ниже (для перемещения по списку используйте стрелки)</i>
""")
