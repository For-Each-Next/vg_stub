"""A class representing and formatting multilingual names."""

from __future__ import annotations

__all__ = ("Name",)

import mwparserfromhell

from vg_stub._utils import pinyin, romaji

ITALIC_LANGS = frozenset(("en",))


class Name:
    """Represents game title in a certain language.

    It with optional transliteration, sorting, and literal translation.

    Mainly supports English, Chinese, and Japanese, with providing
    language-specific transliterations, sortable keys, and a {{langx}}
    template representation.

    Examples:
        >>> zh = Name("zh", "時空幻境")
        >>> zh.name
        '時空幻境'
        >>> zh.sortkey
        'Shi Kong Huan Jing'
        >>> en = Name("en", "Tales of Phantasia", lit="幻想传奇")
        >>> en.sortkey
        'Tales Of Phantasia'
        >>> en.langx
        '{{langx|en|Tales of Phantasia|lit=幻想传奇|italic=yes}}'
        >>> ja = Name("ja", "テイルズ オブ ファンタジア")
        >>> ja.name
        'テイルズ オブ ファンタジア'
        >>> ja.translit
        'Teiruzu obu Fantajia'
        >>> ja.sortkey
        'Teiruzu Obu Fantajia'
        >>> ja2 = Name(
        ...     "ja",
        ...     "キミのいる未来へ",
        ...     translit="Kimi no Iru Mirai e",
        ... )
        >>> ja2.sortkey
        'Kimi Noiru Mirai E'
        >>> ja2.langx
        '{{langx|ja|キミのいる未来へ|translit=Kimi no Iru Mirai e}}'
    """

    def __init__(
        self,
        lang: str,
        name: str,
        translit: str | None = None,
        sortkey: str | None = None,
        lit: str | None = None,
    ) -> None:
        """Initialize a Name object.

        Args:
            lang: ISO 639-1 language code ('en', 'zh', 'ja').
            name: Original title in its native script.
            translit: Optional explicit transliteration. If omitted,
                an auto-generated value will be set.
            sortkey: Optional explicit sorting key. If omitted, an
                auto-generated value will be set.
            lit: Optional literal translation for use in the {{langx}}
                template.
        """
        self.lang = lang
        self.name = name
        self.translit = self._translit(translit)
        self.sortkey = self._sortkey(sortkey)
        self.lit = lit

    def _translit(self, value: str | None) -> str:
        """Return the transliteration for this name.

        If a value is provided, it is returned unchanged. Otherwise, a
        language-specific transliteration (might not correct) will be
        generated:
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
            return pinyin(self.name)
        if self.lang == "ja":
            return romaji(self.name)
        return self.name

    def _sortkey(self, value: str | None) -> str:
        """Return the sort key used for alphabetical ordering.

        If an explicit sort key is provided, it is returned unchanged.
        Otherwise, a language-specific transliteration (might not
        correct) will be generated:
            - Chinese (zh): Toneless Pinyin, every syllable upper-cased.
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
            return pinyin(self.name, tone=False)
        if self.lang == "ja":
            return romaji(self.name).title()
        return self.translit.title()

    @property
    def italic(self) -> bool:
        """Whether this name should be italicized when formatted.

        Returns:
            True if the language requires italics; otherwise False.
        """
        return self.lang in ITALIC_LANGS

    @property
    def langx(self) -> str | None:
        """Return corresponding {{langx}} template.

        Returns:
            The efn template string, or None if no footnote is needed.
        """
        tl = mwparserfromhell.nodes.Template("langx")
        tl.add(1, self.lang, showkey=False)
        tl.add(2, self.name, showkey=False)
        if self.translit != self.name:
            tl.add("translit", self.translit)
        if self.lit:
            tl.add("lit", self.lit)
        if self.italic:
            tl.add("italic", "yes")
        return str(tl)
