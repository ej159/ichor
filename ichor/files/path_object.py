from abc import ABC, abstractmethod
from pathlib import Path


class PathObject(ABC, object):
    """An abstract base class that is used for anything that has a path (i.e. files or directories)"""

    path: Path

    def __init__(self, path):
        self.path = Path(path)

    def exists(self) -> bool:
        """Determines if the path points to an existing directory or file on the storage drive."""
        return self.path.exists()

    @classmethod
    def check_path(cls, path: Path) -> bool:
        return True

    @abstractmethod
    def move(self, dst) -> None:
        """An abstract method that subclasses need to implement. This is used to move files around."""
