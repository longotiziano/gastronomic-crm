import logging

def start_logger(name: str = "project_logger") -> logging.Logger:
    """
    Given the name of the module, returns the module's logger
    """    
    logger = logging.getLogger(name)
    logger.propagate = True
    return logger

def raise_and_log(message: str, error: Exception, logger: logging.Logger):
    er = f"{message} -> Error: {error}"
    logger.error(er)
    raise type(error)(er)