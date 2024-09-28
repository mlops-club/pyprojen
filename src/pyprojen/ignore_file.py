from typing import (
    TYPE_CHECKING,
    List,
    Optional,
)

from pyprojen.file import (
    FileBase,
    IResolver,
)
from pyprojen.util import normalize_persisted_path

if TYPE_CHECKING:
    from pyprojen.project import Project


class IgnoreFile(FileBase):
    def __init__(
        self,
        project: "Project",
        file_path: str,
        filter_comment_lines: bool = True,
        filter_empty_lines: bool = True,
        ignore_patterns: Optional[List[str]] = None,
    ):
        super().__init__(project, file_path, edit_gitignore=False)
        self.filter_comment_lines = filter_comment_lines
        self.filter_empty_lines = filter_empty_lines
        self._patterns: List[str] = ignore_patterns.copy() if ignore_patterns else []

    def add_patterns(self, *patterns: str):
        for pattern in patterns:
            is_comment = pattern.startswith("#")
            is_empty_line = len(pattern.strip()) == 0
            if is_comment and self.filter_comment_lines:
                continue
            if is_empty_line and self.filter_empty_lines:
                continue
            if not is_comment and not is_empty_line:
                self._normalize_patterns(pattern)

            normalized_pattern = normalize_persisted_path(pattern)
            self._patterns.append(normalized_pattern)

    def _normalize_patterns(self, pattern: str):
        opposite = "!" + pattern[1:] if pattern.startswith("!") else "!" + pattern
        self._remove(pattern)  # prevent duplicates
        self._remove(opposite)

        if pattern.endswith("/"):
            prefix = opposite
            self._patterns = [p for p in self._patterns if not p.startswith(prefix)]

    def remove_patterns(self, *patterns: str):
        for p in patterns:
            self._remove(p)

    def exclude(self, *patterns: str):
        return self.add_patterns(*patterns)

    def include(self, *patterns: str):
        for pattern in patterns:
            if not pattern.startswith("!"):
                pattern = "!" + pattern
            self.add_patterns(pattern)

    def synthesize_content(self, resolver: IResolver) -> Optional[str]:
        lines = []
        if self.marker:
            lines.append(f"# {self.marker}")
        lines.extend(self._patterns)
        resolved_lines = resolver.resolve(lines)
        return "\n".join(resolved_lines) + "\n"

    def _remove(self, value: str):
        try:
            self._patterns.remove(value)
        except ValueError:
            pass
