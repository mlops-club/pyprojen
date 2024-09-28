from typing import (
    Any,
    Dict,
    Optional,
)

from pyprojen.constructs import Construct
from pyprojen.util.constructs import (
    find_closest_project,
    is_component,
    tag_as_component,
)


class Component(Construct):
    """
    Represents a project component.
    """

    _auto_ids: Dict[Any, int] = {}

    @staticmethod
    def is_component(x: Any) -> bool:
        """
        Test whether the given construct is a component.

        :param x: The construct to test
        :return: True if the construct is a component, False otherwise
        """
        return is_component(x)

    def __init__(self, scope: Any, id: Optional[str] = None):
        """
        Initialize a Component.

        :param scope: The scope in which to define this component
        :param id: Unique id of the component
        """
        super().__init__(scope, id or f"{self.__class__.__name__}#{self._component_id(scope)}")
        tag_as_component(self)
        self.node.add_metadata("type", "component")
        self.node.add_metadata("construct", self.__class__.__name__)
        self.project = find_closest_project(scope)

    @classmethod
    def _component_id(cls, scope: Any) -> str:
        """
        Generate a unique component ID.

        :param scope: The scope for the component
        :return: A unique component ID
        """
        next_id = cls._auto_ids.get(scope, 0) + 1
        cls._auto_ids[scope] = next_id
        return f"AutoId{next_id}"

    def pre_synthesize(self):
        """
        Called before synthesis.
        """

    def synthesize(self):
        """
        Synthesizes files to the project output directory.
        """

    def post_synthesize(self):
        """
        Called after synthesis.
        """
