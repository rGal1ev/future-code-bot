from .main import router as main
from .task import router as task
from .test import router as test

__all__ = [
    "main",
    "task",
    "test"
]
