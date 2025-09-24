import logging

def get_streaming_logger(name: str) -> logging.Logger:
    """ Any tasks that run in a virtualenv need to create their own streaming logger instance."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())

    return logger