import shutil
import sys
import os
from functools import wraps
from itertools import zip_longest
from pathlib import Path
from typing import Any

from ichor.typing import F

def convert_to_path(func: F) -> F:
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        if func.__annotations__:
            args = list(args)
            annotations = func.__annotations__.items()
            for i, ((annotation, type_), arg) in enumerate(
                zip_longest(annotations, args)
            ):
                if annotation and arg:
                    if type_ is Path and not isinstance(arg, Path):
                        args[i] = Path(arg)
            for kw, arg in kwargs.items():
                if kw in func.__annotations__.keys():
                    if func.__annotations__[kw] is Path:
                        kwargs[kw] = Path(arg)
        return func(*args, **kwargs)

    return wrapper


@convert_to_path
def mkdir(path: Path, empty: bool = False, force: bool = True) -> None:
    if path.is_dir() and empty:
        try:
            shutil.rmtree(path)
        except OSError as err:
            if force:
                print(str(err))
                sys.exit(1)
    path.mkdir(parents=True, exist_ok=not empty)


@convert_to_path
def move(src: Path, dst: Path) -> None:
    src.replace(dst)


@convert_to_path
def cp(src: Path, dst: Path) -> None:
    shutil.copy2(src, dst)


@convert_to_path
def recursive_move(src: Path, dst: Path) -> None:
    if src.isdir():
        for f in src.iterdir():
            if f.isdir() and (dst / f.name).exists():
                recursive_move(f, dst / f.name)
            else:
                move(f, dst)
    else:
        move(f, dst)


@convert_to_path
def remove(path: Path) -> None:
    """ param <path> could either be relative or absolute. """
    if path.exists():
        if path.isfile() or path.islink():
            path.unlink()  # remove the file
        elif os.path.isdir(path):
            shutil.rmtree(path)  # remove dir and all contains
        else:
            raise ValueError(f"file {path} is not a file or dir.")
