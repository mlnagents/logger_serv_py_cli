import time

from .client import ServLogger, get_jsonable_arg

serv_log = ServLogger("log_func")


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
                logger_level = getattr(serv_log, level)
            except Exception as error:
                logger_level = serv_log.error
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