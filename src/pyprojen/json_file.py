import json
from typing import (
    Any,
    Optional,
)

from pyprojen.object_file import ObjectFile


class JsonFile(ObjectFile):
    def __init__(
        self,
        scope: Any,
        file_path: str,
        obj: Any,
        omit_empty: bool = False,
        newline: bool = True,
        allow_comments: Optional[bool] = None,
        *,
        committed: bool = True,
        readonly: bool = True,
    ):
        super().__init__(scope, file_path, obj, omit_empty, committed=committed, readonly=readonly)
        self.newline = newline
        self.supports_comments = (
            allow_comments if allow_comments is not None else file_path.lower().endswith(("json5", "jsonc"))
        )

    def synthesize_content(self, resolver: Any) -> Optional[str]:
        content = super().synthesize_content(resolver)
        if content is None:
            return None

        json_obj = json.loads(content)

        if self.marker:
            if self.supports_comments:
                return f"// {self.marker}\n{self.serialize(json_obj)}"
            else:
                json_obj["//"] = self.marker
                return self.serialize(json_obj)

        return self.serialize(json_obj)

    def serialize(self, obj: Any) -> str:
        content = json.dumps(obj, indent=2)
        if self.newline:
            content += "\n"
        return content
