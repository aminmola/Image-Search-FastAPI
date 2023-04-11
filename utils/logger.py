import json
import inspect
import requests
from enum import Enum
import utils.helper as hp
import utils.config as cfg
from datetime import datetime


class LoggerFormat(Enum):
    """
    Enum for logger formats
    """
    JSON = 0
    STRING = 1


class LoggerLevel(Enum):
    """
    Enum for logger levels
    """
    NOTSET = 0
    DEBUG = 1
    INFO = 2
    WARNING = 3
    ERROR = 4
    CRITICAL = 5


class Logger(object):
    """
    Log string and messages on kafka
    """

    def __init__(self, app_name: str) -> None:
        """
        Initialize logger class
        """
        self._app_name = app_name
        level = cfg.LOGGER_LEVEL.upper()
        self._log_level = LoggerLevel[level] if level in LoggerLevel.__members__ else LoggerLevel.NOTSET
        self.url = cfg.SPLUNK_URL

        self.headers = {
            'Authorization': f'Splunk {cfg.SPLUNK_KEY}',
            'Content-Type': 'text/plain'
        }

    def log(self, level: str, msg: str, **kwargs) -> bool:
        """
        Log messages with different levels
        level: Log level
        msg: Log message
        **kwargs: More parameters for logging message
        Returns: Log string message or log message on kafka message broker
        """
        if 'func' in kwargs:
            func_object = kwargs['func']
            file = inspect.getfile(func_object)
            func = func_object.__name__
        else:
            file = inspect.stack()[2].filename
            func = inspect.stack()[2].function
        log_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        if LoggerLevel[level].value >= self._log_level.value:
            logger_format = cfg.LOGGER_FORMAT.lower()
            if logger_format == LoggerFormat.JSON.name.lower():
                doc = {
                    "time": hp.datetime_to_unix(log_time, date_time_format='%Y-%m-%d %H:%M:%S'),
                    "host": cfg.SPLUNK_HOST,
                    "source": cfg.SPLUNK_SOURCE,
                    "event": {
                        "MESSAGE": msg,
                        "LEVEL": level,
                        "FUNC": func,
                        "FILE": file,
                        "SERVICE": self._app_name
                    }
                }
                if cfg.LOGGER_TYPE == "persist":
                    response = requests.request("POST", self.url,
                                                headers=self.headers,
                                                data=json.dumps(doc))
                    if response.status_code == 200:
                        return True
                else:
                    "TODO: have to add not persist print on terminal "
                    pass
            elif logger_format == LoggerFormat.STRING.name.lower():
                print(f'{log_time} {level} | message: {msg}, file: {file}, function: {func}')
                return True
            else:
                print('Logger format is not correct!')
                return False

    def debug(self, msg: str, **kwargs) -> bool:
        """
        Log debug message
        msg: Log message
        **kwargs: More parameters for debug message
        Returns: Log debug massage based on string or json type
        """
        return self.log(level=LoggerLevel.DEBUG.name, msg=msg, **kwargs)

    def info(self, msg: str, **kwargs) -> bool:
        """
        Log info message
        msg: Log message
        **kwargs: More parameters for info message
        Returns: Log info massage based on string or json type
        """
        return self.log(level=LoggerLevel.INFO.name, msg=msg, **kwargs)

    def error(self, msg: str, **kwargs) -> None:
        """
        Log error message
        msg: Log message
        **kwargs: More parameters for error message
        Returns: Log error massage based on string or json type
        """
        self.log(level=LoggerLevel.ERROR.name, msg=msg, **kwargs)
        raise ValueError(msg)

    def warning(self, msg: str, **kwargs) -> bool:
        """
        Log warning message
        msg: Log message
        **kwargs: More parameters for warning message
        Returns: Log warning massage based on string or json type
        """
        return self.log(level=LoggerLevel.WARNING.name, msg=msg, **kwargs)

    def critical(self, msg: str, **kwargs) -> None:
        """
        Log critical message
        msg: Log message
        **kwargs: More parameters for critical message
        Returns: Log critical massage based on string or json type
        """
        self.log(level=LoggerLevel.CRITICAL.name, msg=msg, **kwargs)
        raise ValueError(msg)
