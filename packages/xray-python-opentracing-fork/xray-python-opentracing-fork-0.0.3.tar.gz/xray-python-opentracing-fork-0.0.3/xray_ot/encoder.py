import traceback
from typing import Any, Type


def default_encoder(o: Any) -> Any:
    kind: Type[Any] = type(o)

    if issubclass(kind, BaseException):
        o: BaseException
        tb = o.__traceback__
        result = {
            "exception": o.__class__.__name__,
            "traceback": traceback.format_tb(tb),
            "message": str(o),
        }
        return result

    raise TypeError(
        f"Object of type {o.__class__.__name__} is not JSON serializable"
    )
