from typing import (
    Any,
    Dict,
)


def remove_null_or_undefined_properties(obj: Dict[str, Any]) -> Dict[str, Any]:
    """
    Remove null or undefined properties from a dictionary.

    :param obj: The input dictionary
    :return: A new dictionary with null or undefined properties removed
    """
    return {k: v for k, v in obj.items() if v is not None}
