from repository.repository_log import TestLogger

def get_logger(tag: str) -> TestLogger:
    return TestLogger(tag)