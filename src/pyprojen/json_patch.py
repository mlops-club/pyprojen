from typing import Any, List
import json
from enum import Enum

class JsonPatchOperation(Enum):
    """Enum for JSON Patch operations."""

    ADD = "add"
    REMOVE = "remove"
    REPLACE = "replace"
    MOVE = "move"
    COPY = "copy"
    TEST = "test"

class JsonPatch:
    """Represents a JSON Patch operation."""

    def __init__(self, op: JsonPatchOperation, path: str, value: Any = None, from_: str = None):
        """
        Initialize a JsonPatch.

        :param op: The operation type
        :param path: The path to apply the operation
        :param value: The value for the operation (if applicable)
        :param from_: The source path for move and copy operations
        """
        self._op = op
        self._path = path
        self._value = value
        self._from = from_

    @staticmethod
    def add(path: str, value: Any) -> 'JsonPatch':
        """
        Create an 'add' JSON Patch operation.

        :param path: The path to add the value
        :param value: The value to add
        :return: A JsonPatch instance
        """
        return JsonPatch(JsonPatchOperation.ADD, path, value)

    @staticmethod
    def remove(path: str) -> 'JsonPatch':
        """
        Create a 'remove' JSON Patch operation.

        :param path: The path to remove
        :return: A JsonPatch instance
        """
        return JsonPatch(JsonPatchOperation.REMOVE, path)

    @staticmethod
    def replace(path: str, value: Any) -> 'JsonPatch':
        """
        Create a 'replace' JSON Patch operation.

        :param path: The path to replace
        :param value: The new value
        :return: A JsonPatch instance
        """
        return JsonPatch(JsonPatchOperation.REPLACE, path, value)

    @staticmethod
    def move(from_: str, path: str) -> 'JsonPatch':
        """
        Create a 'move' JSON Patch operation.

        :param from_: The source path
        :param path: The destination path
        :return: A JsonPatch instance
        """
        return JsonPatch(JsonPatchOperation.MOVE, path, from_=from_)

    @staticmethod
    def copy(from_: str, path: str) -> 'JsonPatch':
        """
        Create a 'copy' JSON Patch operation.

        :param from_: The source path
        :param path: The destination path
        :return: A JsonPatch instance
        """
        return JsonPatch(JsonPatchOperation.COPY, path, from_=from_)

    @staticmethod
    def test(path: str, value: Any) -> 'JsonPatch':
        """
        Create a 'test' JSON Patch operation.

        :param path: The path to test
        :param value: The value to test against
        :return: A JsonPatch instance
        """
        return JsonPatch(JsonPatchOperation.TEST, path, value)

    @staticmethod
    def apply(obj: Any, *patches: 'JsonPatch') -> Any:
        """
        Apply JSON Patch operations to an object.

        :param obj: The object to patch
        :param patches: The patches to apply
        :return: The patched object
        """
        patch_list = [patch._to_dict() for patch in patches]
        return json.loads(json.dumps(obj))  # Create a deep copy
        # In a real implementation, you would apply the patches here
        # This is a placeholder for the actual patch application logic

    def _to_dict(self) -> dict:
        """
        Convert the JsonPatch to a dictionary.

        :return: The dictionary representation of the JsonPatch
        """
        result = {"op": self._op.value, "path": self._path}
        if self._value is not None:
            result["value"] = self._value
        if self._from is not None:
            result["from"] = self._from
        return result