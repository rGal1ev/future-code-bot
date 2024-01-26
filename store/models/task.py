from dataclasses import dataclass


@dataclass
class Task:
    id: int
    title: str
    number: int
    min_answers_count: int
    module_id: int
