from abc import abstractmethod
from types import TracebackType
from typing import Optional, Type, TypeVar

# stdlib-only: this package has no dependencies, and typing.Self needs 3.11 while it supports 3.9
AllocatedT = TypeVar('AllocatedT', bound='Allocated')


class Allocated:
    """ resource allocated on remote host that needs to be free """

    def __init__(self) -> None:
        self._deallocated = False

    def __enter__(self: AllocatedT) -> AllocatedT:
        return self

    def __exit__(self, exc_type: Optional[Type[BaseException]], exc_val: Optional[BaseException],
                 exc_tb: Optional[TracebackType]) -> None:
        self.deallocate()

    @abstractmethod
    def _deallocate(self) -> None:
        pass

    def deallocate(self) -> None:
        if not self._deallocated:
            self._deallocated = True
            self._deallocate()
