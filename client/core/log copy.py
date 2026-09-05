import logging

format = '{asctime} - {levelname:<8} | {message} | {filename}:{lineno} ({funcName}, {taskName})'

logging.basicConfig(style='{', level=logging.NOTSET, format=format, handlers=[
    logging.FileHandler('logs/debug.log'),
    logging.StreamHandler()
])



if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")
