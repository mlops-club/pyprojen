# Copyright (c) HashiCorp, Inc.
# SPDX-License-Identifier: MPL-2.0

from typing import (
    Any,
    Optional,
)

import yaml

from pyprojen.object_file import ObjectFile


class YamlFile(ObjectFile):
    """
    Represents a YAML file.
    """

    def __init__(
        self,
        scope: Any,
        file_path: str,
        obj: Any,
        omit_empty: bool = False,
        line_width: int = 0,
        *,
        committed: bool = True,
        readonly: bool = True,
    ):
        super().__init__(scope, file_path, obj, omit_empty, committed=committed, readonly=readonly)
        self.line_width = line_width

    def synthesize_content(self, resolver: Any) -> Optional[str]:
        content = super().synthesize_content(resolver)
        if content is None:
            return None

        yaml_content = self.serialize(yaml.safe_load(content))

        if self.marker:
            return f"# {self.marker}\n\n{yaml_content}"
        return yaml_content

    def serialize(self, obj: Any) -> str:
        return yaml.dump(obj, default_flow_style=False, width=self.line_width)
