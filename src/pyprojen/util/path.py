def ensure_relative_path_starts_with_dot(path: str) -> str:
    """
    Ensure that a relative path starts with a dot.

    :param path: The input path
    :return: The path with a leading dot if it's relative
    """
    if path.startswith("."):
        return path

    if path.startswith("/"):
        raise ValueError(f"Path {path} must be relative")

    return f"./{path}"
