from __future__ import annotations


class LocalObjectStore:
    def __init__(self) -> None:
        self._objects: dict[str, str] = {}

    def put_text(self, key: str, content: str) -> str:
        self._objects[key] = content
        return key

    def get_text(self, key: str) -> str:
        return self._objects[key]

