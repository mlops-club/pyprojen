from typing import Any
from .object_file import ObjectFile
import toml

class TomlFile(ObjectFile):
    """
    Represents a TOML file.
    """

    def serialize(self, obj: Any) -> str:
        """
        Serialize the object to a TOML string.

        :param obj: The object to serialize
        :return: The serialized TOML string
        """
        return toml.dumps(obj)