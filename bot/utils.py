from aiogram_dialog.widgets.common.when import Predicate


def _not(key: str) -> Predicate:
    def f(data, whenable, manager):
        return not data.get(key)

    return f


def _and(*keys: str) -> Predicate:
    def f(data, whenable, manager):
        accumulator = None

        for key in keys:
            value = bool(data.get(key))

            if key[0] == "!":
                value = not bool(data.get(key[1:]))

            if not accumulator:
                accumulator = value
                continue

            accumulator = accumulator and value

        return accumulator

    return f


def _or(*keys: str) -> Predicate:
    def f(data, whenable, manager):
        accumulator = bool(data.get(keys[0]))

        for key in keys:
            if accumulator:
                break

            accumulator = accumulator or data.get(key)
        return accumulator

    return f


def _get(key):
    def f(item: dict):
        try:
            return item.get(key)

        except AttributeError:
            return None

    return f
