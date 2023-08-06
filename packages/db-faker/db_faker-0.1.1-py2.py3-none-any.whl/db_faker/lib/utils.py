import os
import db_faker

from pathlib import Path


def get_root_path() -> Path:
    """
    Returns the root path of the module
    """
    return Path(db_faker.__file__).parent.parent


def file_exists(path: str) -> bool:
    """
    Returns a boolean indicating if the file referenced by a string pathname do exist
    """
    if os.path.isabs(path):
        abs_path = Path(path)
    else:
        abs_path = Path.cwd().joinpath(path).resolve()

    return abs_path.is_file()


def file_not_exists(path: str) -> bool:
    """
    Returns a boolean indicating if the file referenced by a string pathname do not exist.
    """
    if os.path.isabs(path):
        abs_path = Path(path)
    else:
        abs_path = Path.cwd().joinpath(path).resolve()

    return not abs_path.exists()


def get_file_abs_path(path: str) -> Path:
    """
    Returns the absolute path of the provided string path
    """
    return Path(path) if os.path.isabs(path) else Path.cwd().joinpath(path).resolve()
