from aiogram.fsm.state import StatesGroup, State


class MainWindow(StatesGroup):
    main = State()


class TaskWindow(StatesGroup):
    list = State()
    preview = State()

    new_module = State()
    new_task = State()

    task_answers_edit = State()
    task_answer_edit = State()

    alert = State()
    form = State()


class TestWindow(StatesGroup):
    list = State()
    preview = State()

    answers_edit = State()
    answer_edit = State()

    alert = State()
