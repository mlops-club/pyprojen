import glob
import json
import os
import tempfile
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
)

if TYPE_CHECKING:
    from pyprojen.project import Project


class SnapshotOptions:
    """Options for creating a snapshot."""

    def __init__(self, parse_json: bool = True):
        """
        Initialize SnapshotOptions.

        :param parse_json: Whether to parse JSON files
        """
        self.parse_json = parse_json


def synth_snapshot(project: "Project", options: SnapshotOptions = SnapshotOptions()) -> Dict[str, Any]:
    """
    Create a snapshot of the synthesized project.

    :param project: The project to snapshot
    :param options: Options for creating the snapshot
    :return: A dictionary representing the snapshot
    """
    if not project.outdir.startswith(tempfile.gettempdir()) and "project-temp-dir" not in project.outdir:
        raise ValueError(
            "Trying to capture a snapshot of a project outside of tmpdir, which implies this test might corrupt an existing project"
        )

    if hasattr(project, "_synthed"):
        raise ValueError("duplicate synth()")

    project._synthed = True

    old_env = os.environ.get("PROJEN_DISABLE_POST")
    try:
        os.environ["PROJEN_DISABLE_POST"] = "true"
        project.synth()
        ignore_exts = ["png", "ico"]
        return directory_snapshot(
            project.outdir,
            {
                **options.__dict__,
                "exclude_globs": [f"**/*.{ext}" for ext in ignore_exts],
                "support_json_comments": any(
                    getattr(file, "supports_comments", False) for file in project.files if isinstance(file, JsonFile)
                ),
            },
        )
    finally:
        if old_env is None:
            del os.environ["PROJEN_DISABLE_POST"]
        else:
            os.environ["PROJEN_DISABLE_POST"] = old_env


def directory_snapshot(root: str, options: Dict[str, Any] = {}) -> Dict[str, Any]:
    """
    Create a snapshot of a directory.

    :param root: The root directory to snapshot
    :param options: Options for creating the snapshot
    :return: A dictionary representing the snapshot
    """
    output = {}
    files = glob.glob("**", recursive=True, root_dir=root)
    files = [
        f
        for f in files
        if not f.startswith(".git/") and not any(f.endswith(ext) for ext in options.get("exclude_globs", []))
    ]

    parse_json = options.get("parse_json", True)

    for file in files:
        file_path = os.path.join(root, file)
        if os.path.isfile(file_path):
            if options.get("only_file_names", False):
                output[file] = True
            else:
                with open(file_path, "r") as f:
                    content = f.read()
                    if parse_json and file.lower().endswith((".json", ".json5", ".jsonc")):
                        try:
                            content = json.loads(content)
                        except json.JSONDecodeError:
                            pass  # Keep content as string if it's not valid JSON
                output[file] = content

    return output
