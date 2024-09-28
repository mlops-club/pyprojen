# Import and export from constructs.py
from .constructs import (
    find_closest_project,
    is_component,
    is_project,
    tag_as,
    tag_as_component,
    tag_as_project,
    try_find_closest,
)

# Import and export from name.py
from .name import (
    file_safe_name,
    workflow_name_for_project,
)

# Import and export from object.py
from .object import remove_null_or_undefined_properties

# Import and export from path.py
from .path import ensure_relative_path_starts_with_dot

# Import and export from semver.py
from .semver import (
    TargetName,
    parse_version,
    to_bracket_notation,
    to_maven_version_range,
    to_nuget_version_range,
    to_python_version_range,
    to_release_version,
)

# Import and export from synth.py
from .synth import (
    SnapshotOptions,
    directory_snapshot,
    synth_snapshot,
)

# Import and export from tasks.py
from .tasks import make_cross_platform

# Add these new imports
from .util import deep_merge  # Add this line
from .util import (
    any_selected,
    assert_executable_permissions,
    decamelize,
    decamelize_keys_recursively,
    dedup_array,
    exec,
    exec_capture,
    exec_or_undefined,
    find_up,
    format_as_python_module,
    get_file_permissions,
    get_git_version,
    get_node_major_version,
    is_executable,
    is_object,
    is_root,
    is_truthy,
    is_writable,
    kebab_case_keys,
    multiple_selected,
    normalize_persisted_path,
    snake_case_keys,
    sorted_dict_or_list,
    try_read_file,
    try_read_file_sync,
    write_file,
)

# Export all imported names
__all__ = [
    # constructs.py
    "try_find_closest",
    "find_closest_project",
    "is_project",
    "is_component",
    "tag_as",
    "tag_as_project",
    "tag_as_component",
    # semver.py
    "TargetName",
    "to_maven_version_range",
    "to_nuget_version_range",
    "to_python_version_range",
    "to_release_version",
    "to_bracket_notation",
    "parse_version",
    # object.py
    "remove_null_or_undefined_properties",
    # tasks.py
    "make_cross_platform",
    # synth.py
    "SnapshotOptions",
    "synth_snapshot",
    "directory_snapshot",
    # path.py
    "ensure_relative_path_starts_with_dot",
    # name.py
    "workflow_name_for_project",
    "file_safe_name",
    # util.py
    "is_writable",
    "normalize_persisted_path",
    "try_read_file_sync",
    "write_file",
]
