import json
from typing import Any
from .object_file import ObjectFile

class JsonFile(ObjectFile):
    def serialize(self, obj: Any) -> str:
        return json.dumps(obj, indent=2)