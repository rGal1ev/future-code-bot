from aiogram_dialog.widgets.text import Jinja

list_window_template = Jinja("""
<b>📝 Промежуточные аттестации</b>

{% if is_module_selected %}
─────────
✦ Выбран <b>{{ selected_module["number"] }}</b> модуль
➤ <b>{{ selected_module["title"] }}</b>
─────────
{% else %}
❶ Выберите модуль
{% endif %}
""")

answer_edit_window_template = Jinja("""
💡 <b>Ответ аттестации</b>
▼ <b>Заполните все данные ниже</b>

❶ <b>Номер ответа</b>: {{ number if number else 'Не указано' }}
❷ <b>Ответ</b>: {{ '' if value else 'Не указано' }}
{% if value %}
<pre language="python">{{ value }}</pre>
{% endif %}

<i>Для изменения полей, нажмите на кнопку и введите значение</i>
""")

test_preview_window_template = Jinja("""
{% if not selected_answer %}
Выберите вопрос ниже ▼
{% else %}
<pre language="python">{{ selected_answer["value"] }}</pre>
{% endif %}
""")
