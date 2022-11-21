import logging

from opentelemetry.trace import Status, StatusCode, get_current_span


class LogErrorHandler(logging.Handler):
    def emit(self, record):
        span = get_current_span()
        if span is not None:
            if record.exc_info is not None:
                exc_type, exc_value, tb = record.exc_info
                if exc_value is not None:
                    span.record_exception(exc_value)
            if record.levelno >= logging.ERROR:
                span.set_status(Status(StatusCode.ERROR, record.getMessage()))


def get_logger(name):
    logger = logging.getLogger(name)
    logger.addHandler(LogErrorHandler())
    logger.setLevel(logging.INFO)
    return logger
