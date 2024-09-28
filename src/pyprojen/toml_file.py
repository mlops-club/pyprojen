# Copyright (c) HashiCorp, Inc.
# SPDX-License-Identifier: MPL-2.0

from typing import (
    Any,
    Optional,
)

import tomlkit

from pyprojen.object_file import ObjectFile


class TomlFile(ObjectFile):
    def __init__(
        self,
        scope: Any,
        file_path: str,
        obj: Any,
        omit_empty: bool = False,
        *,
        committed: bool = True,
        readonly: bool = True,
    ):
        super().__init__(scope, file_path, obj, omit_empty, committed=committed, readonly=readonly)

    def synthesize_content(self, resolver: Any) -> Optional[str]:
        content = super().synthesize_content(resolver)
        if content is None:
            return None

        toml_content = self.serialize(tomlkit.loads(content))

        if self.marker:
            return f"# {self.marker}\n\n{toml_content}"
        return toml_content

    def serialize(self, obj: Any) -> str:
        return tomlkit.dumps(obj)
