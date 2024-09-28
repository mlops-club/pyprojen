import hashlib
import re
from abc import (
    ABC,
    abstractmethod,
)
from enum import Enum
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Set,
    Union,
)

from .dependency import (
    Dependable,
    IDependable,
)

CONSTRUCT_SYM = "constructs.Construct"


class IConstruct(IDependable):
    """Interface for constructs."""

    @property
    @abstractmethod
    def node(self) -> "Node":
        """The tree node."""


class ConstructOrder(Enum):
    """Order in which to return constructs."""

    PREORDER = 1
    POSTORDER = 2


class MetadataEntry:
    """Represents a metadata entry."""

    def __init__(self, type: str, data: Any, trace: Optional[List[str]] = None):
        """
        Initialize a MetadataEntry.

        :param type: The type of metadata
        :param data: The metadata data
        :param trace: Optional trace information
        """
        self.type = type
        self.data = data
        self.trace = trace


class IValidation(ABC):
    """Interface for validation."""

    @abstractmethod
    def validate(self) -> List[str]:
        """
        Validate and return a list of error messages.

        :return: List of error messages
        """


class Node:
    """Represents the construct node in the scope tree."""

    PATH_SEP = "/"

    @staticmethod
    def of(construct: IConstruct) -> "Node":
        """
        Returns the node associated with a construct.

        :param construct: The construct
        :return: The associated node
        """
        return construct.node

    def __init__(self, host: "Construct", scope: Optional[IConstruct], id: str):
        """
        Initialize a Node.

        :param host: The host construct
        :param scope: The scope
        :param id: The ID
        """
        self._host = host
        self.scope = scope
        self.id = self._sanitize_id(id or "")
        self._children: Dict[str, IConstruct] = {}
        self._context: Dict[str, Any] = {}
        self._metadata: List[MetadataEntry] = []
        self._dependencies: Set[IDependable] = set()
        self._default_child: Optional[IConstruct] = None
        self._validations: List[IValidation] = []
        self._addr: Optional[str] = None
        self._locked = False

        if scope and not self.id:
            raise ValueError("Only root constructs may have an empty ID")

        if scope:
            scope.node._add_child(host, self.id)

    @property
    def path(self) -> str:
        """
        The full, absolute path of this construct in the tree.

        :return: The path
        """
        components = [scope.node.id for scope in self.scopes if scope.node.id]
        return self.PATH_SEP.join(components)

    @property
    def scopes(self) -> List[IConstruct]:
        """
        All parent scopes of this construct.

        :return: List of parent scopes
        """
        ret = []
        curr: Optional[IConstruct] = self._host
        while curr:
            ret.insert(0, curr)
            curr = curr.node.scope
        return ret

    @property
    def root(self) -> IConstruct:
        """
        The root of the construct tree.

        :return: The root construct
        """
        return self.scopes[0]

    @property
    def children(self) -> List[IConstruct]:
        """
        All direct children of this construct.

        :return: List of child constructs
        """
        return list(self._children.values())

    def add_metadata(self, type: str, data: Any, options: Dict[str, Any] = {}):
        """
        Adds a metadata entry to this construct.

        :param type: The type of metadata
        :param data: The metadata data
        :param options: Additional options
        """
        if data is None:
            return
        trace = None  # Implement stack trace capture if needed
        self._metadata.append(MetadataEntry(type, data, trace))

    def add_validation(self, validation: IValidation):
        """
        Add a validation to this construct.

        :param validation: The validation to add
        """
        self._validations.append(validation)

    def validate(self) -> List[str]:
        """
        Validate this construct.

        :return: List of validation error messages
        """
        return [error for validation in self._validations for error in validation.validate()]

    def _add_child(self, child: "Construct", child_name: str):
        """
        Add a child construct.

        :param child: The child construct
        :param child_name: The name of the child
        """
        if self._locked:
            raise ValueError(f"Cannot add children to {self.path} during synthesis")
        if child_name in self._children:
            raise ValueError(
                f"There is already a Construct with name '{child_name}' in {self._host.__class__.__name__}"
            )
        self._children[child_name] = child

    @staticmethod
    def _sanitize_id(id: str) -> str:
        """
        Sanitize an ID.

        :param id: The ID to sanitize
        :return: The sanitized ID
        """
        return re.sub(f"{Node.PATH_SEP}", "--", id)

    @property
    def addr(self) -> str:
        """
        Returns an opaque tree-unique address for this construct.

        :return: The address
        """
        if not self._addr:
            self._addr = self._calculate_addr()
        return self._addr

    def _calculate_addr(self) -> str:
        """
        Calculate the address for this construct.

        :return: The calculated address
        """
        components = [c.node.id for c in self.scopes]
        hash_object = hashlib.sha1()
        for c in components:
            if c != "Default":
                hash_object.update(c.encode())
                hash_object.update(b"\n")
        return "c8" + hash_object.hexdigest()

    def find_all(self) -> List[IConstruct]:
        """
        Returns a list of all constructs in the tree, including this node's host and all its descendants.

        :return: List of all constructs
        """
        result = [self._host]
        for child in self._children.values():
            result.extend(child.node.find_all())
        return result

    def try_find_child(self, id: str) -> Optional[IConstruct]:
        """
        Attempts to find a child construct by its id.

        :param id: The id of the child construct to find
        :return: The child construct if found, None otherwise
        """
        return self._children.get(id)


class Construct(IConstruct):
    """Represents a construct."""

    def __init__(self, scope: Optional[Union["Construct", IConstruct]], id: str):
        """
        Initialize a Construct.

        :param scope: The scope in which to define this construct
        :param id: The scoped construct ID
        """
        self._node = Node(self, scope, id)
        Dependable.implement(self, Dependable())

    @property
    def node(self) -> Node:
        """
        The tree node.

        :return: The node
        """
        return self._node

    @staticmethod
    def is_construct(x: Any) -> bool:
        """
        Test whether the given construct is a construct.

        :param x: The object to test
        :return: True if the object is a construct, False otherwise
        """
        return hasattr(x, CONSTRUCT_SYM)

    def __str__(self):
        """
        String representation of the construct.

        :return: The string representation
        """
        return self.node.path or "<root>"


# Mark all instances of 'Construct'
setattr(Construct, CONSTRUCT_SYM, True)
