from typing import (
    List,
    Optional,
)

from pyprojen.constructs import Construct
from pyprojen.file import (
    FileBase,
    IResolver,
)


class TextFile(FileBase):
    """
    Represents a text file.
    """

    def __init__(
        self,
        scope: Construct,
        file_path: str,
        lines: Optional[List[str]] = None,
        committed: Optional[bool] = None,
        edit_gitignore: bool = True,
        readonly: Optional[bool] = None,
        executable: bool = False,
        marker: Optional[bool] = None,
    ):
        """
        Initialize a TextFile.

        :param scope: The scope in which to define this file
        :param file_path: The file path
        :param lines: Initial lines of the file
        :param committed: Whether the file should be committed
        :param edit_gitignore: Whether to edit .gitignore
        :param readonly: Whether the file should be readonly
        :param executable: Whether the file should be executable
        :param marker: Whether to add a marker to the file
        """
        super().__init__(
            scope,
            file_path,
            committed=committed,
            edit_gitignore=edit_gitignore,
            readonly=readonly,
            executable=executable,
            marker=marker,
        )
        self._lines: List[str] = lines or []

    def add_line(self, line: str):
        """
        Adds a line to the text file.

        :param line: the line to add (can use tokens)
        """
        self._lines.append(line)

    def synthesize_content(self, resolver: IResolver) -> Optional[str]:
        """
        Synthesize the content of the text file.

        :param resolver: The resolver to use
        :return: The synthesized content as a string, or None
        """
        return "\n".join(self._lines)
