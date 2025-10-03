"""Utilities."""

__all__ = (
    "chinese_punctation_join",
    "comma_join",
    "semi_comma_join",
    "tuplize",
)

from types import EllipsisType, MappingProxyType, NoneType
from typing import TYPE_CHECKING, Any, Literal, overload

if TYPE_CHECKING:
    from collections.abc import Iterable, Sequence


@overload
def tuplize[T: EllipsisType | NoneType](obj: T) -> T: ...


@overload
def tuplize[T: str | bytes | bytearray](obj: T) -> tuple[T]: ...


@overload
def tuplize[T: Any](obj: Iterable[T]) -> tuple[T]: ...


@overload
def tuplize[T: Any](obj: T) -> tuple[T]: ...


def tuplize(obj):
    """Cast an object to a tuple.

    Arguments:
        obj: Object to convert. ``...`` and ``None`` pass through
            unchanged.

    Returns:
        Original obj if Ellipsis/None, tuple containing obj otherwise.

    Examples:
        >>> tuplize(...)
        Ellipsis
        >>> tuplize("neko")
        ('neko',)
        >>> tuplize(31)
        (31,)
        >>> tuplize(["fire", "bird"])
        ('fire', 'bird')
    """
    if (obj is ...) or (obj is None):
        return obj
    if isinstance(obj, str | bytes | bytearray):
        return (obj,)
    try:
        return tuple(obj)
    except TypeError:
        return (obj,)


def chinese_punctation_join(
    items: Iterable[str],
    punct: Literal["period", "semicolon", "comma", "semi-comma"],
    start: str | None = None,
    end: str | None = None,
) -> str | None:
    """Join a series of strings by given Chinese punctuation.

    Arguments:
        items: The strings to join.
        punct: The punctuation to use, which can be
            'period' for The Chinese juhao ('。'),
            'semicolon' Chinese fenhao ('；'),
            'comma' for Chinese douhao ('，'),
            'semi-comma' for Chinese dunhao ('、').
        start: The prefix of the text.
        end: The suffix of the text.

    Returns:
        The joined text. If no Truly items, then return an empty string.

    Examples:
        >>> names = ["彼得", "保罗", "玛丽"]
        >>> chinese_punctation_join(names, "semi-comma")
        '彼得、保罗、玛丽'
        >>> names.clear()
        >>> chinese_punctation_join(names, "semi-comma")
        ''
    """  # noqa: RUF002
    mapping = MappingProxyType({
        "period": "。",
        "semicolon": "；",  # noqa: RUF001
        "comma": "，",  # noqa: RUF001
        "semi-comma": "、",
    })
    if start is None:
        start = ""
    if end is None:
        end = ""
    filtered_items = filter(None, items)
    return f"{start}{mapping[punct].join(filtered_items)}{end}"


def semi_comma_join(
    __strings: Sequence[str] | None,
    /,
    start: str | None = None,
    end: str | None = None,
) -> str | None:
    """Join a series of strings with semi-comma (i.e., dunhao).

    Arguments:
        __strings: Sequence of strings.
        start: The prefix of the text.
        end: The suffix of the text.

    Returns:
        The text with semi-comma separators.

    Examples:
        >>> semi_comma_join(
        ...     ["天空", "海洋", "大地"],
        ...     start="看，",
        ...     end="！",
        ... )
        '看，天空、海洋、大地！'
    """  # noqa: RUF002
    if __strings is None:
        return None
    return chinese_punctation_join(__strings, "semi-comma", start, end)


def comma_join(
    __strings: Sequence[str],
    /,
    start: str | None = None,
    end: str | None = None,
) -> str | None:
    """Join a series of strings with comma (i.e., douhao).

    Arguments:
        __strings: Sequence of strings.
        start: The prefix of the text.
        end: The suffix of the text.

    Returns:
        The text with comma separators.

    Examples:
        >>> comma_join(
        ...     ["潘金莲", "李瓶儿", "庞春梅"],
        ...     start="话说那",
        ...     end="都是何许人也？",
        ... )
        '话说那潘金莲，李瓶儿，庞春梅都是何许人也？'
    """  # noqa: RUF002
    return chinese_punctation_join(__strings, "comma", start, end)
