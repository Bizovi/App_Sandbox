from typing import List, Dict, Tuple, Optional, NewType, Generator, Union, Callable
from enum import Enum
import hashlib
import os
import shutil
from pathlib import Path

# ======= Declare constants and types ====================
# ========================================================
FileHash = NewType("FileHash", str)
HashesDict = Dict[FileHash, Path]

SourcePath = NewType("SourcePath", Path)
DestPath = NewType("DestPath", Path)

# TODO(Mihai): use the algebraic-data-types (adt) package to make this nice
class ActionType(Enum):
    MOVE = "move"
    COPY = "copy"
    DELETE = "delete"

# TODO(Mihai): bake in the constraints on ActionType using just types
ActionDelete = Tuple[ActionType, DestPath]
ActionMoveOrCopy = Tuple[ActionType, SourcePath, DestPath]
ActionGenerator = Generator[Union[ActionDelete, ActionMoveOrCopy], None, None]

BLOCKSIZE = 65536


# ======= Helper functions ===============================
# ========================================================
def hash_file(path: Path) -> FileHash:
    """Reads in a (full) file as buffer and returns its hash"""
    hasher = hashlib.sha1()
    with path.open("rb") as file:
        buf = file.read(BLOCKSIZE)
        while buf:
            hasher.update(buf)
            buf = file.read(BLOCKSIZE)

    return hasher.hexdigest()


def read_paths_and_hashes(root: Path) -> HashesDict:
    hashes = {}
    for folder, _, files in os.walk(root):
        for fn in files:
            hashes[hash_file(Path(folder) / fn)] = fn
    
    return hashes


# ======= 'Business Logic' / The Core ====================
# ========================================================
def determine_actions(
    src_hashes: HashesDict, 
    dst_hashes: HashesDict, 
    src_folder: SourcePath, 
    dst_folder: DestPath
) -> ActionGenerator:
    for sha, filename in src_hashes.items():
        if sha not in dst_hashes:
            sourcepath = Path(src_folder) / filename
            destpath = Path(dst_folder) / filename
            yield 'copy', sourcepath, destpath
        elif dst_hashes[sha] != filename:
            olddestpath = Path(dst_folder) / dst_hashes.get(sha)
            newdestpath = Path(dst_folder) / filename
            yield 'move', olddestpath, newdestpath
    
    for sha, filename in dst_hashes.items():
        if sha not in src_hashes:
            yield 'delete', dst_folder / filename


# ======= The wrapper / Entrypoint =======================
# ========================================================
def sync(
    source: SourcePath, 
    dest: DestPath
) -> None:
    """Top-level function, i.e. imperative shell (wrapper). Infra as code 
    has this already figured out and covered: init - plan - apply
    
    1. gather inputs (I/O bound operation)
    2. call the functional core (pure function)
    3. apply outputs (I/O bound operation)

    Dependency Injection by adding two new arguments -> Easier to test/ fake:
        reader: Callable,
        filesystem: Callable
    """
    source_hashes = read_paths_and_hashes(source)
    dest_hashes = read_paths_and_hashes(dest)

    actions = determine_actions(source_hashes, dest_hashes, source, dest)

    for action, *paths in actions:
        if action == "copy":
            shutil.copyfile(*paths)
        if action == "move":
            shutil.move(*paths)
        if action == "delete":
            os.remove(paths[0])