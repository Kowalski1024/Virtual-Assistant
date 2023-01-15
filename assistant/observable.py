from typing import TypeVar, MutableMapping, Iterator, Protocol
from collections import UserDict

__all__ = [
    "ObservableDict",
    "MutableMappingMixin"
]


_KT = TypeVar('_KT')
_VT = TypeVar('_VT')
_T_co = TypeVar('_T_co', covariant=True)
_VT_co = TypeVar('_VT_co', covariant=True)


class Observer(Protocol):
    def update_observer(self, data) -> None:
        ...


class MutableMappingMixin(MutableMapping[_KT, _VT]):
    def __init__(self):
        super().__init__()
        self._observers: set[Observer] = set()

    def register(self, observer: Observer):
        self._observers.add(observer)

    def exclude(self, observer: Observer):
        self._observers.discard(observer)

    def __setitem__(self, __k: _KT, __v: _VT) -> None:
        super().__setitem__(__k, __v)

        for observer in self._observers:
            observer.update_observer(self)

    def __delitem__(self, __v: _KT) -> None:
        super().__getitem__(__v)

        for observer in self._observers:
            observer.update_observer(self)

    def __getitem__(self, __k: _KT) -> _VT_co:
        return super().__getitem__(__k)

    def __len__(self) -> int:
        return super().__len__()

    def __iter__(self) -> Iterator[_T_co]:
        return super().__iter__()


class ObservableDict(MutableMappingMixin, UserDict):
    pass
