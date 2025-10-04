"""Utilities."""

from __future__ import annotations

__all__ = (
    "chinese_punctation_join",
    "comma_join",
    "hans",
    "hant",
    "is_same_title",
    "pinyin",
    "romaji",
    "semi_comma_join",
    "tuplize",
    "wikilink",
)

from types import EllipsisType, MappingProxyType, NoneType
from typing import TYPE_CHECKING, Any, Literal, overload

import pykakasi
import pypinyin
from mwparserfromhell.nodes import Wikilink
from zhconv_rs import zhconv

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


def hans(text: str) -> str:
    """Convert Chinese text to Simplified Chinese.

    This function performs character-level conversion to Simplified
    Chinese. It does not handle regional word variations.
    For example, it converts '印表機' to '印表机', but not to '打印机'.

    Args:
        text: The input string to convert.

    Returns:
        A string converted to Simplified Chinese characters.

    Examples:
        >>> hans("海內存知己 天涯若比鄰")
        '海内存知己 天涯若比邻'
        >>> hans("Sony影業")
        'Sony影业'
    """
    return zhconv(text, "zh-hans")


def hant(text: str) -> str:
    """Convert Chinese text to Traditional Chinese.

    This function performs character-level conversion to Traditional
    Chinese. It does not handle regional word variations.
    For example, it converts '打印机' to '打印機', but not to '印表機'.

    Args:
        text: The input string to convert.

    Returns:
        A string converted to Traditional Chinese characters.

    Examples:
        >>> hant("海内存知己 天涯若比邻")
        '海內存知己 天涯若比鄰'
        >>> hant("Sony影业")
        'Sony影業'
    """
    return zhconv(text, "zh-hant")


def is_same_title(__text1: str, __text2: str, /) -> bool:
    """Compare whether two texts represent the same title.

    This is a quick checker for whether two strings refer to the same
    Wikipedia article title.

    It considers Wikipedia-style rules: underscores are treated as
    spaces, and comparison is case-insensitive only for the first
    character.

    It also supports simplified/traditional Chinese conversion by
    attempting to convert each character to simplified individually.
    Regional variants are not considered.

    Args:
        __text1: The first text to compare.
        __text2: The second text to compare.

    Returns:
        True if the titles are considered equivalent, False otherwise.

    Examples:
        >>> is_same_title("this is a pen", "This_is_a_pen")
        True
        >>> is_same_title("東方不敗", "东方不败")
        True
        >>> is_same_title("打印机", "列印機")
        False
    """

    def normalize(text: str, /) -> str:
        text = text.replace("_", " ").lstrip(": ").rstrip()
        text = text[0].lower() + text[1:]
        return hans(text)

    return normalize(__text1) == normalize(__text2)


def wikilink(
    title: str,
    text: str | None = None,
    *,
    force: bool = False,
) -> str:
    """Generate a string representing a Wikipedia link.

    This function avoids redundant display text when the title and the
    link text are effectively the same. For example, it prevents outputs
    like `[[Apple|apple]]` or `[[東方不敗|东方不败]]`, as generating
    `[[apple]]` and `[[东方不败]]` directly. Automatic simplification
    can be disabled by setting `force` to True.

    Args:
        title: The page title.
        text: Optional display text for the link. If None, the title is
            used with replacing underscores with spaces.
        force: If True, use the given title and text directly without
            any kind of simplification.

    Returns:
        A string representing the wikilink.

    Examples:
        >>> wikilink("how_are_you?")
        '[[how are you?]]'
        >>> wikilink("東方不敗", "东方不败")
        '[[东方不败]]'
        >>> wikilink("東方不敗", "东方不败", force=True)
        '[[東方不敗|东方不败]]'
    """
    if force:
        return str(Wikilink(title, text))
    if text is None:
        return str(Wikilink(title.replace("_", " ")))
    if is_same_title(title, text):
        return str(Wikilink(text))
    return str(Wikilink(title, text))


def pinyin(text: str, *, tone: bool = True) -> str:
    """Return Chinese Hanyu Pinyin with capitalization.

    Converts Chinese text to Hanyu Pinyin. Syllables are capitalized and
    separated by spaces. When tone is True, diacritics are included;
    when False, toneless Pinyin is returned.

    Args:
        text: Chinese text in Simplified or Traditional characters.
        tone: If True, include tone marks (for example, "Huàn");
            if False, return toneless Pinyin (for example, "Huan").
            Defaults to True.

    Returns:
        Pinyin string with capitalized, space-separated syllables.

    Examples:
        >>> pinyin("幻想传奇")
        'Huàn Xiǎng Chuán Qí'
        >>> pinyin("幻想传奇", tone=False)
        'Huan Xiang Chuan Qi'
    """
    if tone:
        return " ".join(py[0].capitalize() for py in pypinyin.pinyin(text))
    return " ".join(p.capitalize() for p in pypinyin.lazy_pinyin(text))


def romaji(text: str) -> str:
    """Return modified Hepburn romanization with capitalization.

    Converts Japanese text to romanized form using a modified Hepburn
    scheme. Words are capitalized, while common particles keep their
    conventional forms (e.g., he→e, ha→wa, wo→o; loanword "obu" stays
    lowercase). Segmentation is best-effort and may be imperfect.

    Args:
        text: Japanese text (hiragana, katakana, and/or kanji).

    Returns:
        Romanized with appropriate capitalization.

    Examples:
        >>> romaji("幻想物語")
        'Gensou Monogatari'
        >>> romaji("テイルズ オブ ファンタジア")
        'Teiruzu obu Fantajia'
        >>> romaji("キミのいる未来へ")  # の is incorrectly segmented
        'Kimi Noiru Mirai e'
    """
    # Particle mappings for proper romanization
    modified_hepburn_mapping = {
        "obu": "obu",  # オブ (of)
        "he": "e",  # へ
        "ga": "ga",  # が
        "no": "no",  # の
        "wo": "o",  # を
        "to": "to",  # と
        "ha": "wa",  # は
    }

    converter = pykakasi.kakasi()
    words = converter.convert(text)
    result_words = []
    for word in words:
        hepburn = word["hepburn"].strip()
        if not hepburn:
            continue
        modified_hepburn = modified_hepburn_mapping.get(
            hepburn,
            hepburn.capitalize(),
        )
        result_words.append(modified_hepburn)
    return " ".join(result_words)
