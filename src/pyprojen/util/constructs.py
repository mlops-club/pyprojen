from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Optional,
    TypeVar,
)

if TYPE_CHECKING:
    from pyprojen.project import Project

T = TypeVar("T")

PROJECT_SYMBOL = "pyprojen.Project"
COMPONENT_SYMBOL = "pyprojen.Component"


def try_find_closest(predicate: Callable[[Any], bool]) -> Callable[[Optional[Any]], Optional[T]]:
    def finder(construct: Optional[Any] = None) -> Optional[T]:
        if construct is None:
            return None
        scopes = []
        if node := getattr(construct, "node", None):
            scopes = node.scopes
        # scopes = getattr(construct, 'node', {}).get('scopes', [])
        for scope in reversed(scopes):
            if predicate(scope):
                return scope
        return None

    return finder


def find_closest_project(construct: Any) -> "Project":
    from pyprojen.project import Project  # Avoid circular import

    if is_component(construct):
        return construct.project

    project = try_find_closest(Project.is_project)(construct)
    if not project:
        if node := getattr(construct, "node", None):
            path = node.path if node else ""
            raise ValueError(
                f"{construct.__class__.__name__} at '{path}' "
                f"must be created in the scope of a Project, but no Project was found"
            )

    return project


def is_project(x: Any) -> bool:
    from pyprojen.project import Project  # Avoid circular import

    return Project.is_project(x)


def is_component(x: Any) -> bool:
    return hasattr(x, COMPONENT_SYMBOL)


def tag_as(scope: Any, tag: str) -> None:
    setattr(scope, tag, True)


def tag_as_project(scope: Any) -> None:
    tag_as(scope, PROJECT_SYMBOL)


def tag_as_component(scope: Any) -> None:
    tag_as(scope, COMPONENT_SYMBOL)
