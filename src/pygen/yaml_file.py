from typing import Any
from .object_file import ObjectFile
import yaml

class YamlFile(ObjectFile):
    """
    Represents a YAML file.
    """

    def serialize(self, obj: Any) -> str:
        """
        Serialize the object to a YAML string.

        :param obj: The object to serialize
        :return: The serialized YAML string
        """
        return yaml.dump(obj, default_flow_style=False)