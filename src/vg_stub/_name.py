"""A class representing and formatting multilingual names."""

from __future__ import annotations

__all__ = ("Name",)

import mwparserfromhell
from pykakasi import kakasi
from pypinyin import lazy_pinyin, pinyin

ITALIC_LANGS = frozenset(("en",))


def to_pinyin(text: str, *, tone: bool = True) -> str:
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
        >>> to_pinyin("幻想传奇")
        'Huàn Xiǎng Chuán Qí'
        >>> to_pinyin("幻想传奇", tone=False)
        'Huan Xiang Chuan Qi'
    """
    if tone:
        return " ".join(py[0].capitalize() for py in pinyin(text))
    return " ".join(p.capitalize() for p in lazy_pinyin(text))


def to_romaji(text: str) -> str:
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
        >>> to_romaji("幻想物語")
        'Gensou Monogatari'
        >>> to_romaji("テイルズ オブ ファンタジア")
        'Teiruzu obu Fantajia'
        >>> to_romaji("キミのいる未来へ")  # の is incorrectly segmented
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

    converter = kakasi()
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


class Name:
    """Container for multilingual game title names.

    Provides language-aware transliteration, sort keys, and generation
    of Wikipedia {{efn}} notes with nested {{langx}}. Currently supports
    English, Chinese, and Japanese. English names are italicized when
    formatted; Chinese names do not produce footnotes.

    Examples:
        >>> zh = Name("zh", "時空幻境")
        >>> zh.name
        '時空幻境'
        >>> zh.sortkey
        'Shi Kong Huan Jing'
        >>> en = Name("en", "Tales of Phantasia", lit="幻想传奇")
        >>> en.sortkey
        'Tales Of Phantasia'
        >>> en.efn
        '{{efn|{{langx|en|Tales of Phantasia|lit=幻想传奇|italic=yes}}}}'
        >>> ja = Name("ja", "テイルズ オブ ファンタジア")
        >>> ja.name
        'テイルズ オブ ファンタジア'
        >>> ja.translit
        'Teiruzu obu Fantajia'
        >>> ja.sortkey
        'Teiruzu Obu Fantajia'
        >>> ja2 = Name("ja", "キミのいる未来へ", translit="Kimi no Iru Mirai e")
        >>> ja2.sortkey
        'Kimi Noiru Mirai E'
        >>> ja2.efn
        '{{efn|{{langx|ja|キミのいる未来へ|translit=Kimi no Iru Mirai e}}}}'
    """  # noqa: E501, W505

    def __init__(
        self,
        lang: str,
        name: str,
        translit: str | None = None,
        sortkey: str | None = None,
        lit: str | None = None,
    ) -> None:
        """Initialize a Name with language-aware processing.

        Args:
            lang: ISO 639-1 language code (e.g., 'en', 'zh', 'ja').
            name: The name in its original script.
            translit: Optional explicit transliteration. If None is
                given, it is auto-generated for Chinese (Hanyu Pinyin)
                and Japanese (modified Hepburn).
            sortkey: Optional explicit sort key. If None, it is
                auto-generated according to language-specific rules.
            lit: Optional literal translation of the name, used for
                Wikitext {{efn}} notes appended to the main name.
        """
        self.lang = lang
        self.name = name
        self.translit = self._translit(translit)
        self.sortkey = self._sortkey(sortkey)
        self.lit = lit

    def _translit(self, value: str | None) -> str:
        """Return the transliteration for this name.

        If a value is provided, it is returned unchanged. Otherwise, a
        language-specific transliteration is generated:
            - Chinese (zh): Hanyu Pinyin with tone marks.
            - Japanese (ja): Modified Hepburn romanization.
            - Other languages: The original name is returned.

        Args:
            value: Optional explicit-transliteration value.

        Returns:
            Transliterated version of the name.
        """
        if value:
            return value
        if self.lang == "zh":
            return to_pinyin(self.name)
        if self.lang == "ja":
            return to_romaji(self.name)
        return self.name

    def _sortkey(self, value: str | None) -> str:
        """Return the sort key used for alphabetical ordering.

        If an explicit sort key is provided, it is returned unchanged.
        Otherwise, a language-specific key is generated:
        - Chinese (zh): Toneless Pinyin with each syllable capitalized.
        - Japanese (ja): Title-cased romanization.
        - Other languages: Title-cased transliteration.

        Args:
            value: Explicit sort key value, or None to auto-generate.

        Returns:
            Normalized string suitable for alphabetical sorting.
        """
        if value:
            return value
        if self.lang == "zh":
            return to_pinyin(self.name, tone=False)
        if self.lang == "ja":
            return to_romaji(self.name).title()
        return self.translit.title()

    @property
    def italic(self) -> bool:
        """Whether this name should be italicized when formatted.

        Returns:
            True if the language requires italics; otherwise False.
        """
        return self.lang in ITALIC_LANGS

    @property
    def efn(self) -> str | None:
        """Return a Wikipedia efn template embedding {{langx}}.

        Generates the {{efn}} footnote containing a nested {{langx}}.
        Returns None for Chinese names (no footnote is required).

        Returns:
            The efn template string, or None if no footnote is needed.
        """
        if self.lang == "zh":
            return None
        langx = mwparserfromhell.nodes.Template("langx")
        langx.add(1, self.lang, showkey=False)
        langx.add(2, self.name, showkey=False)
        if self.translit != self.name:
            langx.add("translit", self.translit)
        if self.lit:
            langx.add("lit", self.lit)
        if self.italic:
            langx.add("italic", "yes")
        return f"{{{{efn|{langx}}}}}"
