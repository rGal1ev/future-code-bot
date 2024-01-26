from dataclasses import dataclass


@dataclass
class TaskAnswer:
    id: int
    number: int
    value: str
