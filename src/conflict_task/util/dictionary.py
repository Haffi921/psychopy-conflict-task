from .error import fatal_exit


def get_or_fatal_exit(dictionary: dict, key: str, msg: str):
    if value := dictionary.get(key):
        return value
    else:
        fatal_exit(msg)


def get_type_or_fatal_exit(dictionary: dict, key: str, type_name: object, msg: str):
    value = get_or_fatal_exit(dictionary, key, msg)

    if not isinstance(value, type_name):
        fatal_exit(f"'{key}' must be of type '{type_name}'")

    return value


def get_type(dictionary: dict, key: str, type_name: object, *args, **kwargs):
    if value := dictionary.get(key, *args, **kwargs):
        if not isinstance(value, type_name):
            fatal_exit(f"'{key}' must be of type '{type_name}'")

    return value
