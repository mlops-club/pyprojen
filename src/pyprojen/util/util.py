import os
import platform
import re
import subprocess
from typing import (
    Any,
    Dict,
    List,
    Optional,
)

MAX_BUFFER = 10 * 1024 * 1024


def exec(command: str, options: Dict[str, Any]) -> None:
    # logging.debug(command)
    subprocess.run(
        command,
        shell=True,
        check=True,
        cwd=options["cwd"],
        env=options.get("env"),
        stdout=subprocess.PIPE if options.get("stdio") else None,
        stderr=subprocess.PIPE,
    )


def exec_capture(command: str, options: Dict[str, Any]) -> bytes:
    # logging.debug(command)
    result = subprocess.run(
        command,
        shell=True,
        check=True,
        cwd=options["cwd"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return result.stdout


def exec_or_undefined(command: str, options: Dict[str, Any]) -> Optional[str]:
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            cwd=options["cwd"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        value = result.stdout.strip()
        return value if value else None
    except subprocess.CalledProcessError:
        return None


def get_file_permissions(options: Dict[str, bool]) -> str:
    readonly = options.get("readonly", False)
    executable = options.get("executable", False)
    if readonly and executable:
        return "544"
    elif readonly:
        return "444"
    elif executable:
        return "755"
    else:
        return "644"


def write_file(file_path: str, data: Any, options: Dict[str, bool] = {}) -> None:
    if os.path.exists(file_path):
        os.chmod(file_path, 0o600)

    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w") as f:
        f.write(str(data))

    os.chmod(file_path, int(get_file_permissions(options), 8))


def decamelize_keys_recursively(input_data: Any, opt: Dict[str, Any] = {}) -> Any:
    should_always_decamelize = lambda *args: True
    should_decamelize = opt.get("should_decamelize", should_always_decamelize)
    separator = opt.get("separator", "_")
    path = opt.get("path", [])
    max_depth = opt.get("max_depth", 10)

    if len(path) > max_depth:
        raise ValueError("Decamelled too deeply - check that the input has no circular references")

    if isinstance(input_data, list):
        return [decamelize_keys_recursively(k, {**opt, "path": [*path, str(i)]}) for i, k in enumerate(input_data)]

    if isinstance(input_data, dict):
        mapped_object = {}
        for key, value in input_data.items():
            transformed_key = decamelize(key, separator) if should_decamelize([*path, key], value) else key
            mapped_object[transformed_key] = decamelize_keys_recursively(value, {**opt, "path": [*path, key]})
        return mapped_object

    return input_data


def is_truthy(value: Optional[str]) -> bool:
    return value is not None and value.lower() not in ["null", "undefined", "0", "false", ""]


def is_object(x: Any) -> bool:
    return isinstance(x, dict) and x.__class__ == dict


def deep_merge(objects: List[Optional[Dict[str, Any]]], destructive: bool = False) -> Dict[str, Any]:
    """
    Recursively merge objects together.

    :param objects: List of objects to merge
    :param destructive: Whether to delete keys with None values
    :return: Merged dictionary
    """

    def merge_one(target: Dict[str, Any], source: Dict[str, Any]) -> None:
        for key, value in source.items():
            if isinstance(value, dict):
                if not isinstance(target.get(key), dict):
                    target[key] = value
                if "__$APPEND" in value and isinstance(value["__$APPEND"], list):
                    if isinstance(target.get(key), list):
                        target[key].extend(value["__$APPEND"])
                    else:
                        target[key] = value["__$APPEND"]
                merge_one(target[key], value)
                if isinstance(target[key], dict) and len(target[key]) == 0 and destructive:
                    del target[key]
            elif value is None and destructive:
                del target[key]
            elif value is not None:
                target[key] = value

    others = [obj for obj in objects if obj is not None]
    if not others:
        return {}
    into, *rest = others
    for other in rest:
        merge_one(into, other)
    return into


def dedup_array(array: List[Any]) -> List[Any]:
    return list(dict.fromkeys(array))


def sorted_dict_or_list(x: Any) -> Any:
    if x is None:
        return None
    if isinstance(x, list):
        return sorted(x) if x else None
    if isinstance(x, dict):
        return {k: v for k, v in sorted(x.items())} if x else None
    return x


def format_as_python_module(name: str) -> str:
    return name.replace("-", "_").replace(".", "_")


def get_git_version(git_version_output: str) -> str:
    match = re.search(r"\d+\.\d+\.\d+", git_version_output)
    if not match:
        raise ValueError("Unable to retrieve git version")
    return match.group(0)


def kebab_case_keys(obj: Any, recursive: bool = True) -> Any:
    if not isinstance(obj, (dict, list)) or obj is None:
        return obj

    if isinstance(obj, list):
        return [kebab_case_keys(v, recursive) for v in obj] if recursive else obj

    result = {}
    for k, v in obj.items():
        if recursive:
            v = kebab_case_keys(v, recursive)
        result[re.sub(r"_", "-", decamelize(k))] = v
    return result


def snake_case_keys(obj: Any, recursive: bool = True, exclusive_for_record_keys: List[str] = []) -> Any:
    if not isinstance(obj, (dict, list)) or obj is None:
        return obj

    if isinstance(obj, list):
        return [snake_case_keys(v, recursive, exclusive_for_record_keys) for v in obj] if recursive else obj

    result = {}
    for k, v in obj.items():
        if recursive:
            v = snake_case_keys(v, recursive, exclusive_for_record_keys)
        modified_key = decamelize(k) if not exclusive_for_record_keys or k in exclusive_for_record_keys else k
        result[modified_key] = v
    return result


async def try_read_file(file: str) -> str:
    if not os.path.exists(file):
        return ""
    with open(file, "r") as f:
        return f.read()


def try_read_file_sync(file: str) -> Optional[str]:
    if not os.path.exists(file):
        return None
    with open(file, "r") as f:
        return f.read()


def is_writable(file: str) -> bool:
    return os.access(file, os.W_OK)


def assert_executable_permissions(file_path: str, should_be_executable: bool) -> bool:
    if platform.system() == "Windows":
        return True
    prev_executable = is_executable(file_path)
    return prev_executable == should_be_executable


def is_executable(file: str) -> bool:
    return os.access(file, os.X_OK)


def decamelize(s: str, sep: str = "_") -> str:
    if re.match(r"^[a-z][a-zA-Z0-9]*$", s):
        return re.sub(r"([a-z0-9])([A-Z])", r"\1" + sep + r"\2", s).lower()
    else:
        return s


def get_node_major_version() -> Optional[int]:
    match = re.match(r"(\d+)\.(\d+)\.(\d+)", platform.python_version())
    if match:
        return int(match.group(1))
    return None


def any_selected(options: List[Optional[bool]]) -> bool:
    return any(options)


def multiple_selected(options: List[Optional[bool]]) -> bool:
    return sum(1 for opt in options if opt) > 1


def is_root(dir: str, os_path_lib: Any = os.path) -> bool:
    parent = os_path_lib.dirname(dir)
    return parent == dir


def find_up(look_for: str, cwd: str = os.getcwd()) -> Optional[str]:
    if os.path.exists(os.path.join(cwd, look_for)):
        return cwd
    if is_root(cwd):
        return None
    return find_up(look_for, os.path.dirname(cwd))


def normalize_persisted_path(p: str) -> str:
    return p.replace("\\", "/")
