import os
from abc import ABC
from typing import (
    Any,
    Dict,
    List,
    Optional,
)

from pyprojen.cleanup import (
    FILE_MANIFEST,
    cleanup,
)
from pyprojen.common import FILE_MANIFEST
from pyprojen.component import Component
from pyprojen.constructs import Construct
from pyprojen.file import FileBase
from pyprojen.ignore_file import IgnoreFile
from pyprojen.json_file import JsonFile
from pyprojen.object_file import ObjectFile
from pyprojen.util.constructs import tag_as_project

# from pyprojen.gitattributes import GitAttributesFile
# from pyprojen.tasks import Tasks
# from pyprojen.dependencies import Dependencies
# from pyprojen.logger import Logger

DEFAULT_OUTDIR = "."

PROJECT_SYMBOL = "pyprojen.Project"


class Project(Construct, ABC):
    """
    Base project class.
    """

    def __init__(
        self,
        name: str,
        parent: Optional["Project"] = None,
        outdir: str = ".",
        logging: Optional[Dict[str, Any]] = None,
        commit_generated: bool = True,
        git_ignore_filter_comment_lines: bool = True,
        git_ignore_filter_empty_lines: bool = True,
        git_ignore_patterns: Optional[List[str]] = None,
    ):
        """
        Initialize a Project.

        :param name: Project name
        :param parent: Parent project, if any
        :param outdir: Output directory
        :param logging: Logging options
        :param commit_generated: Whether to commit generated files
        :param git_ignore_filter_comment_lines: Whether to filter comment lines in .gitignore
        :param git_ignore_filter_empty_lines: Whether to filter empty lines in .gitignore
        :param git_ignore_patterns: Initial patterns for .gitignore
        """
        super().__init__(parent, f"{self.__class__.__name__}#{name}@{outdir}")
        tag_as_project(self)
        setattr(self, PROJECT_SYMBOL, True)
        self.name = name
        self.parent = parent
        self.outdir = self._determine_outdir(parent, outdir)
        self.commit_generated = commit_generated
        self._ejected = False  # Changed from self.ejected to self._ejected
        self._manifest_files = set()
        self._exclude_from_cleanup: List[str] = []
        self.gitignore = IgnoreFile(
            self,
            ".gitignore",
            filter_comment_lines=git_ignore_filter_comment_lines,
            filter_empty_lines=git_ignore_filter_empty_lines,
            ignore_patterns=git_ignore_patterns,
        )

    @staticmethod
    def is_project(x: Any) -> bool:
        """
        Test whether the given construct is a project.

        :param x: The construct to test
        :return: True if the construct is a project, False otherwise
        """
        return hasattr(x, PROJECT_SYMBOL)

    @staticmethod
    def of(construct: Any) -> "Project":
        """
        Find the closest ancestor project for given construct.

        :param construct: The construct to find the project for
        :return: The closest ancestor project
        :raises ValueError: If no project is found
        """
        if Project.is_project(construct):
            return construct
        if hasattr(construct, "project"):
            return construct.project
        raise ValueError(f"{construct.__class__.__name__} is not associated with a Project")

    @property
    def root(self) -> "Project":
        """
        The root project.

        :return: The root project
        """
        return self.node.root if Project.is_project(self.node.root) else self

    @property
    def components(self) -> List[Component]:
        """
        Returns all the components within this project.

        :return: List of components
        """
        return [c for c in self.node.children if isinstance(c, Component) and c.project == self]

    @property
    def subprojects(self) -> List["Project"]:
        """
        Returns all the subprojects within this project.

        :return: List of subprojects
        """
        return [c for c in self.node.children if Project.is_project(c)]

    @property
    def files(self) -> List[FileBase]:
        """
        All files in this project.

        :return: List of files
        """
        return sorted([c for c in self.components if isinstance(c, FileBase)], key=lambda f: f.path)

    def try_find_file(self, file_path: str) -> Optional[FileBase]:
        """
        Finds a file at the specified relative path within this project and all its subprojects.

        :param file_path: The file path to search for
        :return: The found file or None
        """
        absolute = os.path.abspath(file_path) if os.path.isabs(file_path) else os.path.join(self.outdir, file_path)
        return next((c for c in self.node.find_all() if isinstance(c, FileBase) and c.absolute_path == absolute), None)

    def try_find_object_file(self, file_path: str) -> Optional[ObjectFile]:
        """
        Finds an object file at the specified relative path within this project and all its subprojects.

        :param file_path: The file path to search for
        :return: The found ObjectFile or None
        :raises TypeError: If a file is found but it's not an ObjectFile
        """
        file = self.try_find_file(file_path)
        if file is not None:
            if isinstance(file, ObjectFile):
                return file
            else:
                raise TypeError(f"found file {file_path} but it is not an ObjectFile. got: {file.__class__.__name__}")
        return None

    def add_git_ignore(self, pattern: str):
        """
        Adds a .gitignore pattern.

        :param pattern: The pattern to add
        """
        self.gitignore.add_patterns(pattern)

    def annotate_generated(self, glob: str):
        """
        Consider a set of files as "generated".

        :param glob: The glob pattern to match
        """
        # Implement this method in derived classes

    def synth(self):
        """
        Synthesize all project files into `outdir`.
        """
        # Generate file manifest
        manifest_files = sorted(list(self._manifest_files))
        JsonFile(self, FILE_MANIFEST, {"files": manifest_files}, omit_empty=True)

        # Cleanup orphaned files
        cleanup(self.outdir, manifest_files, self._exclude_from_cleanup)

        # self.logger.debug("Synthesizing project...")
        self.pre_synthesize()

        for comp in self.components:
            comp.pre_synthesize()

        for subproject in self.subprojects:
            subproject.synth()

        for comp in self.components:
            comp.synthesize()

        for comp in self.components:
            comp.post_synthesize()

        self.post_synthesize()

        # self.logger.debug("Synthesis complete")

    def pre_synthesize(self):
        """
        Called before all components are synthesized.
        """

    def post_synthesize(self):
        """
        Called after all components are synthesized.
        """

    @staticmethod
    def _determine_outdir(parent: Optional["Project"], outdir_option: Optional[str]) -> str:
        """
        Determines the output directory for the project.

        :param parent: The parent project, if any
        :param outdir_option: The output directory option
        :return: The determined output directory
        :raises ValueError: If the output directory is invalid
        """
        if parent and os.path.isabs(outdir_option):
            raise ValueError('"outdir" must be a relative path')

        if parent:
            return os.path.abspath(os.path.join(parent.outdir, outdir_option))

        return os.path.abspath(outdir_option)

    def _add_to_manifest(self, file_path: str):
        """
        Adds a file to the manifest.

        :param file_path: The file path to add
        """
        self._manifest_files.add(file_path)

    def add_exclude_from_cleanup(self, *globs: str):
        """
        Exclude the matching files from pre-synth cleanup.

        :param globs: The glob patterns to match
        """
        self._exclude_from_cleanup.extend(globs)

    @property
    def ejected(self) -> bool:
        """
        Whether the project is ejected.

        :return: True if the project is ejected, False otherwise
        """
        return self._ejected
