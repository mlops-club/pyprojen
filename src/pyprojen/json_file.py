import json
from typing import Any
from .object_file import ObjectFile

class JsonFile(ObjectFile):
    """
    Represents a JSON file.
    """

    def serialize(self, obj: Any) -> str:
        """
        Serialize the object to a JSON string.

        :param obj: The object to serialize
        :return: The serialized JSON string
        """
        return json.dumps(obj, indent=2)