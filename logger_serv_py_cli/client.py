import json
import os
import typing as tp
from requests_futures.sessions import FuturesSession
from .utils import get_jsonable_arg, get_data_from_instance, OBJECT_ID, CLASS_NAME

session = FuturesSession()

LOGGER_SERV_LINK = os.environ.get("LOGGER_SERV_LINK")
LOGGER_AUTH_TOKEN = os.environ.get("LOGGER_AUTH_TOKEN")


class LoggerLVL:
    """Уровни отображения для логов."""

    debug = "1"
    info = "2"
    warning = "3"
    error = "4"
    critical = "5"


class ServLogger(object):
    logger_type = "default"

    def __init__(self, logger_type=None):
        if logger_type:
            self.logger_type = logger_type

    def debug(self, *args, **kwargs):
        self.create_log(level=LoggerLVL.debug, *args, **kwargs)

    def info(self, *args, **kwargs):
        self.create_log(level=LoggerLVL.info, *args, **kwargs)

    def warning(self, *args, **kwargs):
        self.create_log(level=LoggerLVL.warning, *args, **kwargs)

    def error(self, *args, **kwargs):
        self.create_log(level=LoggerLVL.error, *args, **kwargs)

    def critical(self, *args, **kwargs):
        self.create_log(level=LoggerLVL.critical, *args, **kwargs)

    def create_log(self, *args, level: str, message: str, data: tp.Optional[tp.Dict[str, tp.Any]] = None, instance=None,  **kwargs):
        if not data:
            data = {}
        forbidden_to_use_keys_if_instance = {CLASS_NAME, OBJECT_ID}
        if set(data.keys()) & forbidden_to_use_keys_if_instance:
            raise Exception(f"Do not use keys {forbidden_to_use_keys_if_instance} in data dict.")
        data.update(**get_data_from_instance(instance))
        if args:
            data["args"] = [get_jsonable_arg(arg) for arg in args]
        if kwargs:
            data["kwargs"] = {key: get_jsonable_arg(value) for key, value in kwargs.items()}

        response = session.post(
            url=LOGGER_SERV_LINK,
            headers={"Authorization": LOGGER_AUTH_TOKEN},
            data={
                "lvl": level,
                "logger_type": self.logger_type,
                "message": message,
                "data": json.dumps(data),
            }
        )
        return response
