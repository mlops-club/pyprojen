from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pyprojen.project import Project


def workflow_name_for_project(base: str, project: "Project") -> str:
    if project.parent:
        return f"{base}_{file_safe_name(project.name)}"
    return base


def file_safe_name(name: str) -> str:
    return name.replace("@", "").replace("/", "-")
