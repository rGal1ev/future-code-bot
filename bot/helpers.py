from store.models import Task, TaskAnswer
from random import sample


def generate_task_solution(task: Task, task_answers: list[TaskAnswer]):
    random_answers = sample(task_answers, task.min_answers_count)
    random_answers.sort(key=lambda item: item.number)

    random_string_answers = []

    for answer in random_answers:
        random_string_answers.append(f"#{answer.number}\n{answer.value}\n\n")

    return ''.join(random_string_answers)
