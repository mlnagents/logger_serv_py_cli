import json
import os
import logging

import requests
import typing as tp
import datetime as dt
import time

logger = logging.getLogger(__name__)

"""
export LOGGER_SERV_LINK=http://127.0.0.1:8080/api/v1/log
export LOGGER_AUTH_TOKEN=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwcm9qZWN0IjoiMSIsInJlYWxtIjoiMiJ9.TWtvPxqM1Xh8U-W9T88232OOE6kvMgxodAa6OIO2Eqs
"""

LOGGER_SERV_LINK = os.environ.get("LOGGER_SERV_LINK")
LOGGER_AUTH_TOKEN = os.environ.get("LOGGER_AUTH_TOKEN")

OBJECT_ID = "obj_id"
CLASS_NAME = "class_name"


class LoggerLVL:
    """Уровни отображения для логов."""

    debug = "1"
    info = "2"
    warning = "3"
    error = "4"
    critical = "5"


def get_changed_values_data(
        old_data: tp.Dict[str, tp.Any], new_data: tp.Dict[str, tp.Any]
) -> tp.Tuple[tp.Dict[str, tp.Any], tp.Dict[str, tp.Any]]:
    """Возвращает ключи и значения словарей, которые поменялись."""
    old_values, new_values = {}, {}
    for key, new_value in new_data.items():
        old_value = old_data.get(key, None)
        if isinstance(new_value, dt.datetime):
            continue
        if old_value != new_value:
            old_values[key] = old_data[key]
            new_values[key] = new_value
    return old_values, new_values


def get_jsonable_arg(x):
    try:
        json.dumps(x)
        return x
    except (TypeError, OverflowError):
        print('q =', type(x).__name__, x)
        return type(x).__name__


class ServLogger(object):
    logger_type = "default"

    def __init__(self, logger_type=None):
        if logger_type:
            self.logger_type = logger_type
        return

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

    @staticmethod
    def get_data_from_instance(instance):
        if instance:
            instance_data = {
                CLASS_NAME: instance.__class__.__name__,
                OBJECT_ID: instance.id if hasattr(instance, "id") else None,
            }

            return instance_data
        return {}

    def create_log(self, level: str, msg: str, data, instance=None, *args, **kwargs):
        forbidden_to_use_keys_if_instance = {CLASS_NAME, OBJECT_ID}
        if set(data.keys()) & forbidden_to_use_keys_if_instance:
            raise Exception(f"Do not use keys {forbidden_to_use_keys_if_instance} in data dict.")
        data.update(**self.get_data_from_instance(instance))
        if args:
            data["args"] = [get_jsonable_arg(arg) for arg in args]
        if kwargs:
            data["kwargs"] = {key: get_jsonable_arg(value) for key, value in kwargs.items()}
        json_data = json.dumps(data)
        form_data = {
            "lvl": level,
            "logger_type": self.logger_type,
            "msg": msg,
            "data": json_data,
        }
        headers = {"Authorization": LOGGER_AUTH_TOKEN}
        response = requests.post(url=LOGGER_SERV_LINK, headers=headers, data=form_data)
        return response


function_logger = ServLogger("log_func")


def log_function(level: str = "info", msg="Log func", is_class_method: bool = False):
    """
    Вешается на функцию или метод класса с атрибутом.

    Если метод класса модели с аргументом self - можно добавить флаг is_class_method=True, тогда данные распарсятся.
        Особенно актуально для джанги.
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            data = {"func": func.__name__}
            error, result = None, None
            start = time.time()
            try:
                result = func(*args, **kwargs)
                logger_level = getattr(function_logger, level)
            except Exception as error:
                logger_level = function_logger.error
                data["err"] = str(error)

            data["time"] = time.time() - start
            if args or kwargs:
                data["in"] = {}
            if args:
                data["in"]["args"] = [get_jsonable_arg(arg) for arg in args]
            if kwargs:
                data["in"]["kwargs"] = {key: get_jsonable_arg(value) for key, value in kwargs.items()}
            if result:
                data["out"] = result
            logger_level(msg=msg, instance=args[0] if is_class_method else None, data=data)
            return result

        return wrapper

    return decorator
