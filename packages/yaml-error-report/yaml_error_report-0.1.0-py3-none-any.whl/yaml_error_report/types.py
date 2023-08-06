from typing import Sequence, Union
from pathlib import Path
import dataclasses


AnyPath = Union[str, Path]
JsonPath = Sequence[Union[str, int]]


@dataclasses.dataclass
class Location:
    ln: int
    col: int
    end_ln: int
    end_col: int
    pos: int
    end_pos: int
    filename: str
