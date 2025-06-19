from services.service_log import TestLogger

def get_logger(tag: str) -> TestLogger:
    return TestLogger(tag)