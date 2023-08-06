__all__ = (
    "NoResult",
    "NoResultType",
)

import enum
import resultful

from typing import (
    Literal,
    Final,
)


class NoResultType(enum.Enum):

    NO_RESULT = enum.auto()

    def __repr__(self) -> str:
        return f"{resultful.__name__}.NoResult"

    # noinspection PyTypeChecker
    def __bool__(self) -> Literal[False]:
        return False


NoResult: Final[Literal[NoResultType.NO_RESULT]] = NoResultType.NO_RESULT
