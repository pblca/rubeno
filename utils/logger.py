import logging


def log_setup(name):
    dt_fmt = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    _log = logging.getLogger(name)
    _log.addHandler(handler)
    _log.setLevel(logging.INFO)

    return _log
