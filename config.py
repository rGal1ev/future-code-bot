from os import getenv


class Config:
    is_dev: bool = True

    def __init__(self):
        if getenv("MODE") == "PROD":
            self.is_dev = False
