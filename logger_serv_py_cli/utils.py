import datetime as dt
import typing as tp
import json


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
    """
    Возвращает объекты, которые могут быть превращены в json,
    в обратном случае возвращают имя объекта.
    """
    try:
        json.dumps(x)
        return x
    except (TypeError, OverflowError):
        return type(x).__name__