from random import sample


def generate_task_solution(task: dict, task_answers: list[dict]):
    if len(task_answers) < task["min_answers_count"]:
        return "empty"

    random_answers = sample(task_answers, task["min_answers_count"])
    random_answers.sort(key=lambda item: item["number"])

    random_string_answers = []

    for answer in random_answers:
        random_string_answers.append(f"#{answer['number']}\n{answer['value']}\n\n")

    return ''.join(random_string_answers)
