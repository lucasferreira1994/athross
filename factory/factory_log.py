<<<<<<< HEAD
from repository.repository_log import TestLogger
=======
from services.service_log import TestLogger
>>>>>>> 584054f2643d394146b28b1a7904c5d83a34115a

def get_logger(tag: str) -> TestLogger:
    return TestLogger(tag)