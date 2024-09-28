from enum import Enum
from typing import (
    Any,
    Dict,
)

import jsonpatch


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

    def __init__(self, operation: str, path: str, value: Any = None, from_: str = None):
        """
        Initialize a JsonPatch.

        :param operation: The operation type
        :param path: The path to apply the operation
        :param value: The value for the operation (if applicable)
        :param from_: The source path for move and copy operations
        """
        self.operation = operation
        self.path = path
        self.value = value
        self.from_ = from_

    @staticmethod
    def add(path: str, value: Any) -> "JsonPatch":
        """
        Create an 'add' JSON Patch operation.

        :param path: The path to add the value
        :param value: The value to add
        :return: A JsonPatch instance
        """
        return JsonPatch("add", path, value)

    @staticmethod
    def remove(path: str) -> "JsonPatch":
        """
        Create a 'remove' JSON Patch operation.

        :param path: The path to remove
        :return: A JsonPatch instance
        """
        return JsonPatch("remove", path)

    @staticmethod
    def replace(path: str, value: Any) -> "JsonPatch":
        """
        Create a 'replace' JSON Patch operation.

        :param path: The path to replace
        :param value: The new value
        :return: A JsonPatch instance
        """
        return JsonPatch("replace", path, value)

    @staticmethod
    def move(from_: str, path: str) -> "JsonPatch":
        """
        Create a 'move' JSON Patch operation.

        :param from_: The source path
        :param path: The destination path
        :return: A JsonPatch instance
        """
        return JsonPatch("move", path, from_=from_)

    @staticmethod
    def copy(from_: str, path: str) -> "JsonPatch":
        """
        Create a 'copy' JSON Patch operation.

        :param from_: The source path
        :param path: The destination path
        :return: A JsonPatch instance
        """
        return JsonPatch("copy", path, from_=from_)

    @staticmethod
    def test(path: str, value: Any) -> "JsonPatch":
        """
        Create a 'test' JSON Patch operation.

        :param path: The path to test
        :param value: The value to test against
        :return: A JsonPatch instance
        """
        return JsonPatch("test", path, value)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the JsonPatch to a dictionary.

        :return: The dictionary representation of the JsonPatch
        """
        patch_dict = {"op": self.operation, "path": self.path}
        if self.value is not None:
            patch_dict["value"] = self.value
        if self.from_ is not None:
            patch_dict["from"] = self.from_
        return patch_dict

    @staticmethod
    def apply(obj: Any, *patches: "JsonPatch") -> Any:
        """
        Apply JSON Patch operations to an object.

        :param obj: The object to patch
        :param patches: The patches to apply
        :return: The patched object
        """
        patch_list = [patch.to_dict() for patch in patches]
        return jsonpatch.apply_patch(obj, patch_list)
