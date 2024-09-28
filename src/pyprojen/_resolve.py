import re
from typing import (
    Any,
    Dict,
)


class IResolvable:
    def to_json(self) -> Any:
        raise NotImplementedError()


def is_resolvable(obj: Any) -> bool:
    return hasattr(obj, "to_json") and callable(getattr(obj, "to_json"))


def resolve(value: Any, options: Dict[str, Any] = {}) -> Any:
    """
    Recursively resolves a value, handling various Python types and custom resolvable objects.

    Args:
        value (Any): The value to resolve. Can be of any type.
        options (Dict[str, Any], optional): Additional options for resolution. Defaults to {}.
            - 'args' (List): Arguments to pass to callable values.
            - 'omit_empty' (bool): If True, empty lists and dicts are resolved to None.

    Returns:
        Any: The resolved value.

    Raises:
        ValueError: If a regular expression with flags is encountered.
    """
    args = options.get("args", [])
    omit_empty = options.get("omit_empty", False)

    match value:
        case None:
            return None
        case _ if is_resolvable(value):
            return resolve(value.to_json(), options)
        case re.Pattern():
            if value.flags:
                raise ValueError("RegExp with flags should be explicitly converted to a string")
            return value.pattern
        case set():
            return resolve(list(value), options)
        case dict():
            result = {}
            for k, v in value.items():
                resolved = resolve(v, options)
                if resolved is not None:
                    result[k] = resolved
            return None if omit_empty and not result else result
        case list():
            resolved = [x for x in (resolve(v, options) for v in value) if x is not None]
            return None if omit_empty and not resolved else resolved
        case _ if callable(value):
            return resolve(value(*args), options)
        case _:
            return value
