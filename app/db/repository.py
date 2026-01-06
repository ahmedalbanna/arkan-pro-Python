from typing import Generic, TypeVar

T = TypeVar("T")

class Repository(Generic[T]):
    # Example base repository pattern
    def __init__(self):
        self._items: dict[str, T] = {}

    def add(self, id: str, item: T) -> T:
        self._items[id] = item
        return item

    def get(self, id: str) -> T | None:
        return self._items.get(id)

    def list(self) -> list[T]:
        return list(self._items.values())

    def delete(self, id: str) -> None:
        self._items.pop(id, None)
