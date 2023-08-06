__all__ = (
    "Result",
    "AlwaysSuccess",
    "AlwaysFailure",
    "ResultType",
    "NoResultType",
    "unsafe",
    "success",
    "failure",
    "unwrap_success",
    "unwrap_failure",
    "NoResult",
)

# Annotations

from .result import (
    Result,
    AlwaysSuccess,
    AlwaysFailure,
)

# Types

from .result import (
    ResultType,
    NoResultType,
)

# Concretes

from .result import (
    unsafe,
    success,
    failure,
    unwrap_success,
    unwrap_failure,
    NoResult,
)
