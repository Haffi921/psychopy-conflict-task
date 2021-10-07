from psychopy import core, logging


def fatal_exit(msg: str):
    logging.fatal(msg)
    core.quit()


def true_or_fatal_exit(test: bool, msg: str):
    if not test:
        fatal_exit(msg)
