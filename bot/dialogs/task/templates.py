from aiogram_dialog.widgets.text import Jinja

main_window_template = Jinja("""
<b>📝 Самостоятельные работы</b>

{% if is_module_selected %}
{% if selected_module %}
─────────
✦ Выбран <b>{{ selected_module.number }}</b> модуль
➤ <b>{{ selected_module.title }}</b>
{% endif %}
{% if is_task_selected %}
───
✦ Выбрана <b>{{ selected_task.number }}</b> работа 
➤ <b>{{ selected_task.title }}</b>
─────────

▼ Получить ответ
{% else %}

❷ Выберите самостоятельную работу
{% endif %}

{% else %}
❶ Выберите модуль
{% endif %}
""")

new_module_window_template = Jinja("""
<b>Напишите название и номер модуля</b>

<b>Пример:</b>
<code>Ведение:1</code>

{% if message %}
<b>Последнее сообщение</b>:
<code>{{ message }}</code>
{% endif %}
""")

new_task_window_template = Jinja("""
▼ <b>Заполните все данные ниже</b>

❶ <b>Номер работы</b>: {{ number if number else 'Не указано' }}
❷ <b>Название</b>: {{ title if title else 'Не указано' }}
❸ <b>Минимальное количество ответов</b>: {{ min_answers_count if min_answers_count else 'Не указано' }}

<i>Для изменения полей, нажмите на кнопку и введите значение</i>
""")

task_answer_edit_window_template = Jinja("""
▼ <b>Заполните все данные ниже</b>

❶ <b>Номер работы</b>: {{ number if number else 'Не указано' }}
❷ <b>Ответ</b>: {{ '' if value else 'Не указано' }}
{% if value %}
<pre language="python">{{ value }}</pre>
{% endif %}

<i>Для изменения полей, нажмите на кнопку и введите значение</i>
""")
