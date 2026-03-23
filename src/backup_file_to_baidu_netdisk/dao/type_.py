from pathlib import Path
from typing import Any, TypeAlias

PathObj:TypeAlias = str | Path

DependencyContext:TypeAlias = dict[str,Any]