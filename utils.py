CURRENT_LEVEL = "INFO"

from wpilib import DataLogManager
def log_exception(e):
    DataLogManager.log(repr(e))

LOG_LEVELS = {
    "DEBUG": 0,
    "INFO": 1,
    "WARNING": 2,
    "ERROR": 3,
    "CRITICAL": 4
}

LOG_LEVEL = LOG_LEVELS[CURRENT_LEVEL]

def debug_log(message):
    if LOG_LEVEL <= LOG_LEVELS["DEBUG"]:
        print(message)

def info_log(message):
    if LOG_LEVEL <= LOG_LEVELS["INFO"]:
        print(message)
        
def warning_log(message):
    if LOG_LEVEL <= LOG_LEVELS["WARNING"]:
        print(message)
        
def error_log(message):
    if LOG_LEVEL <= LOG_LEVELS["ERROR"]:
        print(message)        
        
#TODO -> save logs

def clamp(value, min_value, max_value):
    return max(min(value, max_value), min_value)

def for_each(mechanisms_dict, method_name):
    for mechanism in mechanisms_dict.values():
        try:
            if hasattr(mechanism, method_name):
                getattr(mechanism, method_name)()
        except BaseException as e:
            log_exception(e)   