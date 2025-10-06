"""A class representing and formatting multilingual names."""

from __future__ import annotations

__all__ = ("Name",)


import mwparserfromhell

from vg_stub.utils import pinyin, romaji

ITALIC_LANGS = frozenset(("en",))


class Name:
    """Represents a game title in a specific language.

    Supports optional transliteration, sorting keys, and literal
    translations. These can be generated automatically, though the
    results may not always be fully accurate.

    Primarily supports English, Chinese, and Japanese, providing
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
        >>> en.langx()
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
        >>> ja2.langx()
        '{{langx|ja|キミのいる未来へ|translit=Kimi no Iru Mirai e}}'
        >>> ja2.efn(translit=False)
        '{{efn|{{langx|ja|キミのいる未来へ}}}}'
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
            lang: The ISO 639-1 language code ('en', 'zh', 'ja').
            name: The original title in its native script.
            translit: An optional explicit transliteration. If omitted,
                an auto-generated value will be used.
            sortkey: An optional explicit sorting key. If omitted, an
                auto-generated value will be used.
            lit: An optional literal translation for use in the
                {{langx}} and {{efn}} template.
        """
        self.lang = lang
        self.name = name
        self.translit = self._translit(translit)
        self.sortkey = self._sortkey(sortkey)
        self.lit = lit

    def _translit(self, value: str | None) -> str:
        """Return the transliteration for this name.

        If a value is provided, it is returned unchanged. Otherwise, a
        language-specific transliteration (might not be correct) will be
        generated:
            - Chinese (zh): Hanyu Pinyin with tone marks.
            - Japanese (ja): Modified Hepburn romanization.
            - Other languages: The original name is returned.

        Args:
            value: An optional explicit transliteration value.

        Returns:
            The transliterated version of the name.
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
        Otherwise, a language-specific sort key (might not be correct)
        will be generated:
            - Chinese: Toneless Pinyin with every syllable title-cased.
            - Japanese: Title-cased romanization.
            - Other languages: Title-cased transliteration.

        Args:
            value: An explicit sort key value, or None to auto-generate.

        Returns:
            A normalized string suitable for alphabetical sorting.
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

    def langx(
        self,
        *,
        translit: bool = True,
        lit: bool = True,
        italic: bool = True,
    ) -> str:
        """Return the corresponding {{langx}} template.

        Args:
            translit: Whether to include the transliteration.
            lit: Whether to include the literal translation.
            italic: Whether to apply italics for languages that
                italicize work titles.

        Returns:
            The langx template string.
        """
        tl_langx = mwparserfromhell.nodes.Template("langx")
        tl_langx.add(1, self.lang, showkey=False)
        tl_langx.add(2, self.name, showkey=False)
        if translit and (self.translit != self.name):
            tl_langx.add("translit", self.translit)
        if lit and self.lit:
            tl_langx.add("lit", self.lit)
        if italic and self.italic:
            tl_langx.add("italic", "yes")
        return str(tl_langx)

    def efn(
        self,
        *,
        translit: bool = True,
        lit: bool = True,
        italic: bool = True,
    ) -> str:
        """Return the {{efn}} wrapping the {{langx}}.

        Args:
            translit: Whether to include the transliteration in the
                langx template.
            lit: Whether to include the literal translation in the
                langx template.
            italic: Whether to apply italics for languages that
                italicize work titles.

        Returns:
            The efn template string containing the langx template.
        """
        tl_lang = self.langx(translit=translit, lit=lit, italic=italic)
        tl_efn = mwparserfromhell.nodes.Template("efn")
        tl_efn.add(1, tl_lang)
        return str(tl_efn)
