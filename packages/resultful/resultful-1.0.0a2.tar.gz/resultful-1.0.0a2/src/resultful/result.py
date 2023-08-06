__all__ = (
    "unsafe",
    "success",
    "failure",
    "unwrap_success",
    "unwrap_failure",
    "Result",
    "AlwaysSuccess",
    "AlwaysFailure",
    "ResultType",
    "NoResult",
    "NoResultType",
)

from typing import (
    overload,
    TypeVar,
    Tuple,
    Union,
    Final,
)

from resultful.impl.result import (
    Success,
    Failure,
)

from resultful.impl.no_result import (
    NoResult,
    NoResultType,
)

ValueType = TypeVar("ValueType")
ErrorType = TypeVar("ErrorType", bound=BaseException)

Result = Union[Success[ValueType], Failure[ErrorType]]

AlwaysSuccess = Union[Success[ValueType]]
AlwaysFailure = Union[Failure[ErrorType]]

ResultType: Final[Tuple[type, ...]] = (Success, Failure)


# noinspection PyUnresolvedReferences
def unsafe(
    result: Result[ValueType, ErrorType],
) -> ValueType:

    """
    Unwraps the value from given result in unsafe way.

    :param result: result to be unwrapped

    :raises ErrorType: When result is a :class:`Failure`.
    """

    if result:
        return result.value

    raise result.error


# TODO(kprzybyla): Remove "type: ignore" once below feature will be implemented
#                  https://github.com/python/typing/issues/599


@overload
def success(  # type: ignore
    value: Failure[ErrorType],
    /,
) -> NoResultType:
    ...


@overload
def success(
    value: Success[ValueType],
    /,
) -> Success[ValueType]:
    ...


@overload
def success(
    value: ValueType,
    /,
) -> Success[ValueType]:
    ...


def success(  # type: ignore
    value: Union[Failure[ErrorType], Success[ValueType], ValueType],
    /,
) -> Union[NoResultType, Success[ValueType]]:

    """
    Returns value wrapped in :class:`Success`.

    If value is a :class:`Failure`, returns NoResult.
    If value is a :class:`Success`, returns that :class:`Success`.

    :param value: any value
    """

    if isinstance(value, Failure):
        return NoResult

    if isinstance(value, Success):
        return value

    return Success(value)


@overload
def failure(
    error: Success[ValueType],
    /,
) -> NoResultType:
    ...


@overload
def failure(
    error: Failure[ErrorType],
    /,
) -> Failure[ErrorType]:
    ...


@overload
def failure(
    error: ErrorType,
    /,
) -> Failure[ErrorType]:
    ...


def failure(
    error: Union[Success[ValueType], Failure[ErrorType], ErrorType],
    /,
) -> Union[NoResultType, Failure[ErrorType]]:

    """
    Returns error wrapped in :class:`Failure`.

    If error is a :class:`Success`, returns NoResult.
    If error is a :class:`Failure`, returns that :class:`Failure`.

    :param error: any exception
    """

    if isinstance(error, Success):
        return NoResult

    if isinstance(error, Failure):
        return error

    return Failure(error)


@overload
def unwrap_success(
    result: Failure[ErrorType],
) -> NoResultType:
    ...


@overload
def unwrap_success(
    result: Success[ValueType],
) -> ValueType:
    ...


# noinspection PyUnresolvedReferences
def unwrap_success(
    result: Result[ValueType, ErrorType],
) -> Union[NoResultType, ValueType]:

    """
    Unwraps the value from given :class:`Success`.

    :param result: :class:`Success`
    """

    if isinstance(result, Failure):
        return NoResult

    return result.value


@overload
def unwrap_failure(
    result: Success[ValueType],
) -> NoResultType:
    ...


@overload
def unwrap_failure(
    result: Failure[ErrorType],
) -> ErrorType:
    ...


# noinspection PyUnresolvedReferences
def unwrap_failure(
    result: Result[ValueType, ErrorType],
) -> Union[NoResultType, ErrorType]:

    """
    Unwraps the error from given :class:`Failure`.

    :param result: :class:`Failure`
    """

    if isinstance(result, Success):
        return NoResult

    return result.error
