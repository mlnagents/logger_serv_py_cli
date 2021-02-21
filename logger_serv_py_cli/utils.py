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


def get_jsonable_arg(stranger):
    """
    Возвращает объекты, которые могут быть превращены в json,
    в обратном случае возвращают имя объекта.
    """

    try:
        json.dumps(stranger)
        return stranger
    except (TypeError, OverflowError):
        if type(stranger) in {set, list, tuple}:
            result = [get_jsonable_arg(item) for item in stranger]
        elif type(stranger) is dict:
            result = {i: get_jsonable_arg(items) for i, items in enumerate(stranger.items())}
        else:
            result = {"obj": type(stranger).__name__}
            if hasattr(stranger, "pk"):
                result['pk'] = stranger.pk
        return result
