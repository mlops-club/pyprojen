from abc import ABC
from typing import (
    Any,
    List,
    Optional,
)

from pyprojen._resolve import resolve
from pyprojen.file import (
    FileBase,
    IResolver,
)
from pyprojen.json_patch import JsonPatch
from pyprojen.util import deep_merge


class ObjectFile(FileBase, ABC):
    """
    Represents an Object file.
    """

    def __init__(self, scope: Any, file_path: str, obj: Any, omit_empty: bool = False, **kwargs):
        """
        Initialize an ObjectFile.

        :param scope: The scope in which to define this object
        :param file_path: The file path
        :param obj: The object that will be serialized
        :param omit_empty: Omits empty objects and arrays
        :param kwargs: Additional keyword arguments
        """
        super().__init__(scope, file_path, **kwargs)
        self._obj = obj
        self._omit_empty = omit_empty
        self._raw_overrides = {}
        self._patch_operations: List[List[JsonPatch]] = []

    def synthesize_content(self, resolver: IResolver) -> Optional[str]:
        """
        Synthesize the content of the object file.

        :param resolver: The resolver to use
        :return: The synthesized content as a string, or None
        """
        obj = self._obj() if callable(self._obj) else self._obj
        resolved = resolve(obj, {"omit_empty": self._omit_empty})

        if resolved is None:
            return None

        deep_merge([resolved, self._raw_overrides], True)

        patched = resolved
        for patch in self._patch_operations:
            patched = JsonPatch.apply(patched, patch)

        return self.serialize(patched) if patched else None

    def serialize(self, obj: Any) -> str:
        """
        Serialize the object to a string.

        :param obj: The object to serialize
        :return: The serialized object as a string
        """
        raise NotImplementedError("Subclasses must implement this method")

    def add_override(self, path: str, value: Any):
        """
        Adds an override to the synthesized object file.

        :param path: The path of the property
        :param value: The value to set
        """
        parts = self._split_on_periods(path)
        curr = self._raw_overrides

        while len(parts) > 1:
            key = parts.pop(0)
            if key not in curr or not isinstance(curr[key], dict):
                curr[key] = {}
            curr = curr[key]

        curr[parts[0]] = value

    def add_deletion_override(self, path: str):
        """
        Adds a deletion override to the synthesized object file.

        :param path: The path of the property to delete
        """
        self.add_override(path, None)

    def patch(self, *patches: JsonPatch):
        """
        Applies JSON patches to the synthesized object file.

        :param patches: The patches to apply
        """
        self._patch_operations.extend(patches)

    @staticmethod
    def _split_on_periods(x: str) -> List[str]:
        """
        Split a string on periods while processing escape characters.

        :param x: The string to split
        :return: A list of split string parts
        """
        ret = [""]
        for i, char in enumerate(x):
            if char == "\\" and i + 1 < len(x):
                ret[-1] += x[i + 1]
                i += 1
            elif char == ".":
                ret.append("")
            else:
                ret[-1] += char
        return [part for part in ret if part]

    def get_object(self) -> Any:
        """
        Get the raw object before any resolution or patching.

        :return: The raw object
        """
        return self._obj() if callable(self._obj) else self._obj

    def set_object(self, obj: Any):
        """
        Set the raw object.

        :param obj: The new object to set
        """
        self._obj = obj
