from psychopy import logging


def true_or_warn(test: bool, msg: str):
    if not test:
        logging.warning(msg)
    return test
