from abc import (
    ABC,
    abstractmethod,
)
from typing import (
    TYPE_CHECKING,
    List,
)

if TYPE_CHECKING:
    from pyprojen.constructs.construct import IConstruct


class IDependable(ABC):
    pass


class Dependable:
    @staticmethod
    def implement(instance: IDependable, trait: "Dependable") -> None:
        setattr(instance, "_dependable_trait", trait)

    @staticmethod
    def of(instance: IDependable) -> "Dependable":
        trait = getattr(instance, "_dependable_trait", None)
        if trait is None:
            raise ValueError(f"{instance} does not implement IDependable. Use 'Dependable.implement()' to implement")
        return trait

    @property
    @abstractmethod
    def dependency_roots(self) -> List["IConstruct"]:
        pass


class DependencyGroup(IDependable):
    def __init__(self, *deps: IDependable):
        self._deps: List[IDependable] = []

        Dependable.implement(self, self)
        self.add(*deps)

    @property
    def dependency_roots(self) -> List["IConstruct"]:
        result = []
        for d in self._deps:
            result.extend(Dependable.of(d).dependency_roots)
        return result

    def add(self, *scopes: IDependable) -> None:
        self._deps.extend(scopes)
