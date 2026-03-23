from pathlib import Path
from typing import Any, TypeAlias
from typing import TypeVar

PathObj:TypeAlias = str | Path

DependencyContext:TypeAlias = dict[str,Any]



S = TypeVar('S')
D = TypeVar('D')
R = TypeVar('R')
